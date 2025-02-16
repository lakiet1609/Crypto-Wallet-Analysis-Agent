from datetime import datetime, timedelta

from src.utils.logger import logging
from src.config.app_config import CryptoConfig as cc
from src.database.db.wallet_db import CryptoDatabase
from src.utils.common import save_trend_analysis_to_file


class HistoricalTrendAnalysisAgent:
    def __init__(self):
        self.trend_analysis_report_path = cc.trend_analysis_report_path
        self.cryto_db = CryptoDatabase()
        self.collection = self.cryto_db.get_collection()
        self.current_time = datetime.now()
        logging.info('Initialize Historical Trend Analysis')

    
    def get_features(self, wallet_address):
        wallet_data = self.collection.find_one({"wallet_address": wallet_address})
        transaction_history = wallet_data.get("transaction_history", [])
        token_balances = wallet_data.get("token_balances", [])
        return transaction_history, token_balances


    def _filter_transactions_by_timeframe(self, days, transaction_history):
        logging.info("Filter transactions within the specified timeframe.")
        
        timeframe_start = self.current_time - timedelta(days=days)
        return [
            tx for tx in transaction_history
            if datetime.fromtimestamp(tx["timestamp"]) >= timeframe_start
        ]

    def _calculate_portfolio_value_change(self, initial_balances, current_balances):
        logging.info("Calculate the overall portfolio value change.")
        initial_value = sum(initial_balances.values())
        current_value = sum(current_balances.values())
        return current_value - initial_value

    def _identify_notable_asset_changes(self, initial_balances, current_balances):
        logging.info("Identify notable asset acquisitions or sales.")
        
        notable_changes = {}
        for token, initial_balance in initial_balances.items():
            current_balance = current_balances.get(token, 0)
            change = current_balance - initial_balance
            if abs(change) > 0: 
                notable_changes[token] = change
        return notable_changes

    def _get_initial_balances(self, days, token_balances, transaction_history):
        logging.info("Get initial balances at the start of the timeframe.")
        
        timeframe_start = self.current_time - timedelta(days=days)
        initial_balances = {token["symbol"]: token["balance"] for token in token_balances}
        for tx in transaction_history:
            if datetime.fromtimestamp(tx["timestamp"]) < timeframe_start:
                if tx["type"] == "send":
                    initial_balances[tx["token"]] -= tx["amount"]
                elif tx["type"] == "receive":
                    initial_balances[tx["token"]] += tx["amount"]
        return initial_balances

    def _categorize_overall_change(self, change):
        logging.info("Categorize the overall change as increase, decrease, or stable.")
        
        if change > 0:
            return "increase"
        elif change < 0:
            return "decrease"
        else:
            return "stable"


    def _analyze_transaction_patterns(self, transactions):
        logging.info("Analyze transaction patterns (e.g., sends vs. receives).")
        send_count = sum(1 for tx in transactions if tx["type"] == "send")
        receive_count = sum(1 for tx in transactions if tx["type"] == "receive")
        return {
            "send_count": send_count,
            "receive_count": receive_count,
            "net_activity": receive_count - send_count
        }


    def analyze_trends(self, wallet_address):
        logging.info("Analyze trends over 30-day, 90-day, and 180-day timeframes.")
        
        transaction_history, token_balances = self.get_features(wallet_address=wallet_address)

        timeframes = [30, 90, 180]
        results = {}

        for days in timeframes:
            transactions = self._filter_transactions_by_timeframe(days, transaction_history)

            initial_balances = self._get_initial_balances(days, token_balances, transaction_history)
            current_balances = {token["symbol"]: token["balance"] for token in token_balances}

            portfolio_value_change = self._calculate_portfolio_value_change(initial_balances, current_balances)

            notable_asset_changes = self._identify_notable_asset_changes(initial_balances, current_balances)

            transaction_patterns = self._analyze_transaction_patterns(transactions)

            overall_change = self._categorize_overall_change(portfolio_value_change)

            results[f"{days}_day_trend"] = {
                "overall_change": overall_change,
                "notable_changes": notable_asset_changes,
                "transaction_patterns": transaction_patterns
            }

        return results


    def interpret_strategy(self, results):
        logging.info("Interpret the holder's strategy based on trends.")

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

            if data["transaction_patterns"]["net_activity"] > 0:
                strategy_insights.append(f"The wallet has been net receiving assets, indicating inflows.")
            elif data["transaction_patterns"]["net_activity"] < 0:
                strategy_insights.append(f"The wallet has been net sending assets, indicating outflows.")
            else:
                strategy_insights.append(f"The wallet's sending and receiving activity is balanced.")

        return " ".join(strategy_insights)
    

    def get_response(self, wallet_address):
        logging.info('Get result ...')
        
        trend_results = self.analyze_trends(wallet_address)
        conclusion = self.interpret_strategy(trend_results)
        save_trend_analysis_to_file(trend_results=trend_results,
                                    conclusion=conclusion,
                                    filename=self.trend_analysis_report_path)