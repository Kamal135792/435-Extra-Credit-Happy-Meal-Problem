import random
import statistics
import matplotlib.pyplot as plt

def theoretical_standard(n):
    """Calculates theoretical Expected Value and Variance for standard setup."""
    expected_value = n * sum(1/j for j in range(1, n + 1))
    
    sum_inv_sq = sum(1/(j**2) for j in range(1, n))
    sum_inv = sum(1/j for j in range(1, n))
    variance = (n**2 * sum_inv_sq) - (n * sum_inv)
    
    return expected_value, variance

def theoretical_trading(n, r):
    """Calculates theoretical Expected Value and Variance with trading enabled."""
    expected_value = 1
    variance = 0
    
    for k in range(1, n):
        q = k / n
        p = (n - k) / n
        
        ev_stage = (1 - q**r) / p
        expected_value += ev_stage
        
        sec_moment = sum((2*i - 1) * (q**(i-1)) for i in range(1, r + 1))
        var_stage = sec_moment - ev_stage**2
        variance += var_stage
        
    return expected_value, variance

def simulate_standard(n):
    """Simulates a single run of the standard Coupon Collector's Problem."""
    collected = set()
    boxes_opened = 0
    
    while len(collected) < n:
        boxes_opened += 1
        toy = random.randint(1, n)
        collected.add(toy)
        
    return boxes_opened

def simulate_trading(n, r):
    """Simulates a single run with the Trading Mechanic."""
    collected = set()
    boxes_opened = 0
    duplicates = 0
    
    while len(collected) < n:
        boxes_opened += 1
        toy = random.randint(1, n)
        
        if toy in collected:
            duplicates += 1
            if duplicates == r:
                missing_toys = list(set(range(1, n + 1)) - collected)
                collected.add(missing_toys[0])
                duplicates = 0 
        else:
            collected.add(toy)
            
    return boxes_opened

def run_and_plot_simulations(n_values, r_values, trials=1000):
    """Runs simulations across different n and r values and plots the results."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    std_emp_means, std_emp_vars = [], []
    std_theo_means, std_theo_vars = [], []
    
    print("Simulating Standard Problem...")
    for n in n_values:
        results = [simulate_standard(n) for _ in range(trials)]
        std_emp_means.append(statistics.mean(results))
        std_emp_vars.append(statistics.variance(results))
        
        theo_m, theo_v = theoretical_standard(n)
        std_theo_means.append(theo_m)
        std_theo_vars.append(theo_v)
        
    ax1.plot(n_values, std_emp_means, 'k--', label="Standard (Empirical)", linewidth=2)
    ax1.plot(n_values, std_theo_means, 'k:', label="Standard (Theoretical)", linewidth=2, alpha=0.7)
    
    ax2.plot(n_values, std_emp_vars, 'k--', label="Standard (Empirical)", linewidth=2)
    ax2.plot(n_values, std_theo_vars, 'k:', label="Standard (Theoretical)", linewidth=2, alpha=0.7)

    colors = ['b', 'g', 'r', 'm', 'c']
    
    for idx, r in enumerate(r_values):
        print(f"Simulating Trading Mechanic for r={r}...")
        emp_means, emp_vars = [], []
        theo_means, theo_vars = [], []
        color = colors[idx % len(colors)]
        
        for n in n_values:
            results = [simulate_trading(n, r) for _ in range(trials)]
            emp_means.append(statistics.mean(results))
            emp_vars.append(statistics.variance(results))
            
            theo_m, theo_v = theoretical_trading(n, r)
            theo_means.append(theo_m)
            theo_vars.append(theo_v)
            
        ax1.plot(n_values, emp_means, color=color, label=f"Trade r={r} (Empirical)", linewidth=2)
        ax1.plot(n_values, theo_means, color=color, linestyle=':', alpha=0.7)
        
        ax2.plot(n_values, emp_vars, color=color, label=f"Trade r={r} (Empirical)", linewidth=2)
        ax2.plot(n_values, theo_vars, color=color, linestyle=':', alpha=0.7)

    ax1.set_title("Expected Boxes Opened vs. Total Toys (n)")
    ax1.set_xlabel("Total Distinct Toys (n)")
    ax1.set_ylabel("Expected Value (E[T_n])")
    ax1.legend()
    ax1.grid(True)

    ax2.set_title("Variance of Boxes Opened vs. Total Toys (n)")
    ax2.set_xlabel("Total Distinct Toys (n)")
    ax2.set_ylabel("Variance (Var(T_n))")
    ax2.set_yscale('log')
    ax2.legend()
    ax2.grid(True)

    plt.suptitle("Impact of Trade-in Mechanic on the Coupon Collector Problem", fontsize=16)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    n_test_values = [50, 100, 500]
    r_test_values = [10, 25, 50]
    
    run_and_plot_simulations(n_values=n_test_values, r_values=r_test_values, trials=1000)