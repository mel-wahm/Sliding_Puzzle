install:
	@uv sync
run:
	@uv run python -m Src
clean:
	@pyclean .