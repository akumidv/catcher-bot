"""
Forward portfolio - without any limits around strategies entries and exits
"""

from catcher_bot.model.module.portfolio import Portfolio


class ForwardPortfolio(Portfolio):
    """
    Portfolio without any control of risks.
    """

