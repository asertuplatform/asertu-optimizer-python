from asertu.optimizer import Optimizer


def test_import() -> None:
    client = Optimizer(api_key="test")
    result = client.optimize("hello")
    assert result["input"] == "hello"
