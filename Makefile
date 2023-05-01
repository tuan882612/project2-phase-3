.PHONY: run

run:
	@echo "Starting Project2 Phase3 Tkinter App..."
	@. .venv/bin/activate && python src/app.py

clean:
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@echo "Cleaned up __pycache__ directories"