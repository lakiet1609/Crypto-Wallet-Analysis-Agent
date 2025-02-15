from datetime import datetime, timedelta

class HistoricalTrendAnalysisAgent:
    def __init__(self, wallet_data):
        self.wallet_data = wallet_data
        self.current_time = datetime.now()
        self.transaction_history = wallet_data.get("transaction_history", [])
        self.token_balances = wallet_data.get("token_balances", [])
        self.tokens_held = wallet_data.get("tokens_held", [])


    def _filter_transactions_by_timeframe(self, days):
        timeframe_start = self.current_time - timedelta(days=days)
        return [
            tx for tx in self.transaction_history
            if datetime.fromtimestamp(tx["timestamp"]) >= timeframe_start
        ]


    def _calculate_portfolio_value_change(self, initial_balances, current_balances):
        initial_value = sum(initial_balances.values())
        current_value = sum(current_balances.values())
        return current_value - initial_value


    def _identify_notable_asset_changes(self, initial_balances, current_balances):
        notable_changes = {}
        for token, initial_balance in initial_balances.items():
            current_balance = current_balances.get(token, 0)
            change = current_balance - initial_balance
            if abs(change) > 0: 
                notable_changes[token] = change
        return notable_changes


    def _get_initial_balances(self, days):
        timeframe_start = self.current_time - timedelta(days=days)
        initial_balances = {token["symbol"]: token["balance"] for token in self.token_balances}
        for tx in self.transaction_history:
            if datetime.fromtimestamp(tx["timestamp"]) < timeframe_start:
                if tx["type"] == "send":
                    initial_balances[tx["token"]] -= tx["amount"]
                elif tx["type"] == "receive":
                    initial_balances[tx["token"]] += tx["amount"]
        return initial_balances

    def _categorize_overall_change(self, change):
        if change > 0:
            return "increase"
        elif change < 0:
            return "decrease"
        else:
            return "stable"

    def analyze_trends(self):
        timeframes = [30, 90, 180]
        results = {}

        for days in timeframes:
            transactions = self._filter_transactions_by_timeframe(days)

            initial_balances = self._get_initial_balances(days)
            current_balances = {token["symbol"]: token["balance"] for token in self.token_balances}

            portfolio_value_change = self._calculate_portfolio_value_change(initial_balances, current_balances)

            notable_asset_changes = self._identify_notable_asset_changes(initial_balances, current_balances)

            overall_change = self._categorize_overall_change(portfolio_value_change)

            results[f"{days}_day_trend"] = {
                "overall_change": overall_change,
                "notable_changes": notable_asset_changes
            }

        return results

    def interpret_strategy(self, results):
        strategy_insights = []
        for timeframe, data in results.items():
            if data["overall_change"] == "increase":
                strategy_insights.append(f"The portfolio value has increased over the {timeframe.replace('_', '-')} period, suggesting active investment or accumulation.")
            elif data["overall_change"] == "decrease":
                strategy_insights.append(f"The portfolio value has decreased over the {timeframe.replace('_', '-')} period, indicating divestment or profit-taking.")
            else:
                strategy_insights.append(f"The portfolio value has remained stable over the {timeframe.replace('_', '-')} period, suggesting a holding strategy.")

            if data["notable_changes"]:
                strategy_insights.append(f"Notable changes include: {data['notable_changes']}")

        return " ".join(strategy_insights)


       