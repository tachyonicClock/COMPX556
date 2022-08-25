
build_benchmarks:
	# Easy
	cargo run -- partial 0.5 data/complete/LatinSquare08.json data/benchmarks/Easy.json
	# Medium
	cargo run -- partial 0.2 data/complete/LatinSquare15.json data/benchmarks/Medium.json
	# Hard
	cargo run -- partial 0.5 data/complete/LatinSquare15.json data/benchmarks/Hard.json
	# Very Hard
	cargo run -- partial 0.5 data/complete/LatinSquare20.json data/benchmarks/VeryHard.json
	# Impossible
	cargo run -- partial 0.5 data/complete/LatinSquare50.json data/benchmarks/Impossible.json


run_benchmarks:
	# Easy
	cargo run -- solve 0.0 30 data/benchmarks/Easy.json
	# Medium
	cargo run -- solve 0.0 30 data/benchmarks/Medium.json
	# Hard
	cargo run -- solve 0.0 30 data/benchmarks/Hard.json
	# Very Hard
	cargo run -- solve 0.0 30 data/benchmarks/VeryHard.json
	# Impossible
	cargo run -- solve 0.0 30 data/benchmarks/Impossible.json