FLAGS = --secret-file .env
ACT = act $(FLAGS)

.PHONY: test_unit test_integration

test_unit:
	$(ACT) -W .github/workflows/test_unit.yml

test_integration:
	$(ACT) -W .github/workflows/test_integration.yml

test: test_unit test_integration