import argparse
import importlib.util
import json
import sys
from pathlib import Path

# Add strategy directory to sys.path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from base_strategy import BaseStrategy
from strategy_runner import StrategyRunner

def load_strategy_class(strategy_file):
    module_name = Path(strategy_file).stem
    spec = importlib.util.spec_from_file_location(module_name, strategy_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, type) and hasattr(attr, '__bases__'):
            if issubclass(attr, BaseStrategy) and attr is not BaseStrategy:
                return attr
    raise ValueError("No strategy class found in file")

def main():
    parser = argparse.ArgumentParser(description='Run backtest')
    parser.add_argument('strategy_file', help='Strategy filename (e.g., ma_cross_strategy.py)')
    parser.add_argument('--params', type=str, default='{}', help='Strategy parameters as JSON')
    parser.add_argument('--cash', type=float, default=100000, help='Initial cash')
    parser.add_argument('--commission', type=float, default=0.001, help='Commission rate')
    parser.add_argument('--symbols', type=str, required=True, help='Stock symbols (comma-separated)')
    parser.add_argument('--start-date', type=str, required=True, help='Start date (YYYYMMDD)')
    parser.add_argument('--end-date', type=str, required=True, help='End date (YYYYMMDD)')
    parser.add_argument('--output', type=str, default='backtest_results.json', help='Output file')

    args = parser.parse_args()

    impls_dir = Path(__file__).parent / "impls"
    strategy_file = (impls_dir / args.strategy_file).resolve()
    strategy_class = load_strategy_class(strategy_file)
    strategy_params = json.loads(args.params)

    

    runner = StrategyRunner(
        strategy_class,
        live_mode=False,
        cash=args.cash,
        commission=args.commission,
        **strategy_params
    )

    symbols = [s.strip() for s in args.symbols.split(',')]
    runner.fetch_data(symbols, args.start_date, args.end_date)

    runner.run(args.output)

if __name__ == '__main__':
    main()
