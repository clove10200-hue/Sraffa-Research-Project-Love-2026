import sys
import numpy as np
import pathlib
import argparse
from pydantic import BaseModel, ConfigDict, Field

thisdir = pathlib.Path(__file__).parent.resolve()
DAT_DIR = thisdir.parent / "dat"   # Chris's example data files live in <repo>/dat/

class Economy(BaseModel):
    """A simple economy with k commodities and n industries.

    Each industry consumes some amount of each commodity and produces a gross output of one commodity.
    The input data is the matrix M of inputs consumed by each industry, and the vector q of gross outputs.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)  # allow numpy arrays as fields

    names: list[str] = Field(..., description="Names of the commodities (optional)")
    M: np.ndarray = Field(..., description="n x k matrix of inputs consumed by each industry")
    q: np.ndarray = Field(..., description="n-vector of gross outputs produced by each industry")

    def solve(self) -> tuple[float, np.ndarray]:
        """Return (rate_of_profit, prices) for the input matrix M and outputs q.

        Prices are normalized so the first commodity has price 1.

        Returns:
            tuple(float, np.ndarray): 
                A tuple containing an exact solution for the economy's maximum rate of profit and a NumPy vector containing relative prices.

        """
        A = np.diag(1.0 / self.q) @ self.M           # input coefficients: inputs per unit output
        eigvals, eigvecs = np.linalg.eig(A)

        # Perron-Frobenius: pick the largest real eigenvalue with a positive eigenvector.
        idx = int(np.argmax(np.real(eigvals)))
        lam = float(np.real(eigvals[idx]))
        p = np.real(eigvecs[:, idx])
        p = p / p[0]                       # numeraire: price of commodity 0 == 1

        r = 1.0 / lam - 1.0
        return r, p
    
    def power_iteration(self, error: float) -> tuple[float, np.ndarray]:
        '''
        Returns the approximations for (rate_of_profit, prices) for the input matrix M and outputs q using power iteration. Prices are normalized so the
        first commodity has price 1.
        
        Parameters:
            error (float):
                The allowable error for the solutions, as a float between 0 and 1.

        Returns:
            tuple(float, np.ndarray): 
                A tuple containing an approximation for the economy's maximum rate of profit and a NumPy vector containing an approximation of relative prices. Approximates according to the allowable error.
        '''

        A = np.diag(1.0 / self.q) @ self.M  #construct initial coefficient matrix
        x = np.ones(self.q.size)           #initial 'guess' - just a vector of appropriate length full of ones. TODO: a better guessing logic
        x = x / np.linalg.norm(x)
        Ax = A @ x
        rayleigh: float = Ax.dot(x) #because x is normalized to a unit vector, the denominator x1.dot(x1) is simply 1

        while np.linalg.norm(Ax-rayleigh*x) > abs(rayleigh)*error: #termination criteria - the length of the operation A*x - rayleigh*x being less than a certain percentage of the current rayleigh quotient. TODO: Ability to change error to suit user
            x = Ax / np.linalg.norm(Ax)
            Ax = A @ x
            rayleigh = Ax.dot(x) 

        Ax = Ax / Ax[0] #normalize prices to make commodity 1 the numeraire

        r = 1.0 / rayleigh - 1.0 #calculate approximate rate of profit from approximate eigenvalue

        return r, Ax

    def condition_number(self) -> float:
        '''
        Test and debugging method for finding the condition number of an economy's coefficient matrix. Important for numerical
        stability concerns.

        Returns:
            float: 
                A float representing the condition number of the coefficient matrix A.
        '''
        A = np.diag(1.0 / self.q) @ self.M
        cond_num: float = np.linalg.cond(A)
        return cond_num
    
    def add_error(self, error: float) -> "Economy":
        '''
        Method for adding a random error to each element of the coefficient matrix. Returns a new economy object that contains the new M and q matrices with error introduced.
        '''
        rand = np.random.default_rng()
        A = error*self.M
        B = error*self.q
        with np.nditer(A, op_flags=['readwrite']) as it:
            for element in it:
                if element == 0:
                    continue
                random = rand.random()
                sign = rand.choice([-1, 1], 1)
                element[...] =+ random*element*sign
        with np.nditer(B, op_flags=['readwrite']) as it:
            for element in it:
                random = rand.random()
                sign = rand.choice([-1, 1], 1)
                element[...] =+ random*element*sign
        
        return Economy(names=self.names, M=self.M + A, q=self.q + B)
    
    def perturb(self, error):
        mask = self.M != 0
        delta_M = np.random.uniform(-error, error, size=self.M.shape) * mask
        delta_q = np.random.uniform(-error, error, size=self.q.shape) * self.q
        return Economy(names=self.names, M=self.M + delta_M, q=self.q + delta_q)
    
    @staticmethod
    def from_file(path: pathlib.Path) -> "Economy":
        """Read a commodity file. Returns an Economy object.
        
        Args:
            path: Path to the economy file.

        Returns:
            An Economy object containing the names, input matrix M, and output vector q.
        """
        names, rows, outputs = [], [], []
        for line in open(path):
            line = line.split("#", 1)[0].strip()  # drop comments / blank lines
            if not line:
                continue
            if ":" in line:
                label, line = line.split(":", 1)
                names.append(label.strip())
            else:
                names.append(f"commodity_{len(names)}")
            values = [float(x) for x in line.split()]
            rows.append(values[:-1])     # inputs consumed by this industry
            outputs.append(values[-1])   # gross output of this industry
        return Economy(names=names, M=np.array(rows), q=np.array(outputs))

def main():
    parser = argparse.ArgumentParser(
        description="Solve for prices and rate of profit in a simple economy."
    )
    default_path = DAT_DIR / "surplus_1.txt"
    parser.add_argument(
        "path", nargs="?", default=default_path,
        help=f"Path to the economy file (default: {default_path})"
    )
    args = parser.parse_args()

    economy = Economy.from_file(args.path)

    r, p = economy.solve()

    print(f"economy: {args.path}\n")
    print(f"rate of profit r = {r:.4%}\n")
    print("prices:")
    for name, price in zip(economy.names, p):
        print(f"  {name:<16} {price:.4f}")

    # Sanity check: plug the solution back into the original equations.
    lhs = (economy.M @ p) * (1 + r)
    rhs = economy.q * p
    print(f"\nmax residual of (1+r)*M*p == q*p :  {np.max(np.abs(lhs - rhs)):.2e}")


if __name__ == "__main__":
    main()
