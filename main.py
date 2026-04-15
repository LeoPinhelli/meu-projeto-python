from __future__ import annotations

import argparse
import json
import random
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


DATA_FILE = Path(__file__).with_name("learning_plan.json")

SUGGESTIONS = [
	{"name": "Rust", "kind": "linguagem", "difficulty": 4},
	{"name": "FastAPI", "kind": "framework", "difficulty": 3},
	{"name": "TypeScript", "kind": "linguagem", "difficulty": 3},
	{"name": "Docker", "kind": "ferramenta", "difficulty": 2},
	{"name": "pytest", "kind": "ferramenta", "difficulty": 2},
	{"name": "Svelte", "kind": "framework", "difficulty": 3},
]


@dataclass
class Topic:
	id: int
	name: str
	kind: str
	difficulty: int
	completed: bool = False
	created_at: str = date.today().isoformat()


def load_topics() -> list[Topic]:
	if not DATA_FILE.exists():
		return []

	try:
		raw_items = json.loads(DATA_FILE.read_text(encoding="utf-8"))
	except json.JSONDecodeError:
		return []

	topics: list[Topic] = []
	for item in raw_items:
		topics.append(
			Topic(
				id=int(item["id"]),
				name=str(item["name"]),
				kind=str(item["kind"]),
				difficulty=int(item["difficulty"]),
				completed=bool(item.get("completed", False)),
				created_at=str(item.get("created_at", date.today().isoformat())),
			)
		)
	return topics


def save_topics(topics: list[Topic]) -> None:
	DATA_FILE.write_text(
		json.dumps([asdict(topic) for topic in topics], ensure_ascii=False, indent=2),
		encoding="utf-8",
	)


def next_id(topics: list[Topic]) -> int:
	return max((topic.id for topic in topics), default=0) + 1


def format_topic(topic: Topic) -> str:
	status = "feito" if topic.completed else "em aberto"
	return f"#{topic.id} | {topic.name} | {topic.kind} | dificuldade {topic.difficulty} | {status}"


def cmd_add(args: argparse.Namespace) -> None:
	topics = load_topics()
	topic = Topic(
		id=next_id(topics),
		name=args.name,
		kind=args.kind,
		difficulty=args.difficulty,
	)
	topics.append(topic)
	save_topics(topics)
	print(f"Tarefa adicionada: {format_topic(topic)}")


def cmd_list(_: argparse.Namespace) -> None:
	topics = load_topics()
	if not topics:
		print("Nenhuma tarefa cadastrada ainda.")
		return

	for topic in topics:
		print(format_topic(topic))


def cmd_done(args: argparse.Namespace) -> None:
	topics = load_topics()
	for topic in topics:
		if topic.id == args.id:
			topic.completed = True
			save_topics(topics)
			print(f"Marcado como concluido: {format_topic(topic)}")
			return

	print(f"Nenhuma tarefa encontrada com id {args.id}.")


def cmd_stats(_: argparse.Namespace) -> None:
	topics = load_topics()
	total = len(topics)
	completed = sum(topic.completed for topic in topics)
	open_items = total - completed

	print(f"Total: {total}")
	print(f"Concluidos: {completed}")
	print(f"Em aberto: {open_items}")


def cmd_recommend(_: argparse.Namespace) -> None:
	topics = load_topics()
	open_topics = [topic for topic in topics if not topic.completed]

	if open_topics:
		suggestion = sorted(open_topics, key=lambda topic: (topic.difficulty, topic.id))[0]
		print("Proximo foco sugerido:")
		print(format_topic(suggestion))
		return

	suggestion = random.choice(SUGGESTIONS)
	print("Sem tarefas abertas. Uma sugestao para estudar agora:")
	print(
		f"{suggestion['name']} | {suggestion['kind']} | dificuldade {suggestion['difficulty']}"
	)


def cmd_seed(_: argparse.Namespace) -> None:
	topics = load_topics()
	existing = {(topic.name.lower(), topic.kind.lower()) for topic in topics}

	added = 0
	for suggestion in SUGGESTIONS:
		key = (suggestion["name"].lower(), suggestion["kind"].lower())
		if key in existing:
			continue

		topics.append(
			Topic(
				id=next_id(topics),
				name=suggestion["name"],
				kind=suggestion["kind"],
				difficulty=suggestion["difficulty"],
			)
		)
		added += 1

	save_topics(topics)
	print(f"{added} sugestoes adicionadas ao plano.")


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description="Pequena CLI para organizar o aprendizado de uma linguagem ou framework."
	)
	subparsers = parser.add_subparsers(dest="command")

	add_parser = subparsers.add_parser("add", help="Adicionar um novo objetivo de estudo.")
	add_parser.add_argument("name", help="Nome da linguagem, framework ou ferramenta.")
	add_parser.add_argument(
		"kind",
		choices=["linguagem", "framework", "ferramenta"],
		help="Categoria do objetivo.",
	)
	add_parser.add_argument(
		"difficulty",
		type=int,
		choices=range(1, 6),
		help="Dificuldade de 1 a 5.",
	)
	add_parser.set_defaults(func=cmd_add)

	list_parser = subparsers.add_parser("list", help="Listar os objetivos cadastrados.")
	list_parser.set_defaults(func=cmd_list)

	done_parser = subparsers.add_parser("done", help="Marcar um objetivo como concluido.")
	done_parser.add_argument("id", type=int, help="Id do objetivo.")
	done_parser.set_defaults(func=cmd_done)

	stats_parser = subparsers.add_parser("stats", help="Exibir um resumo rapido.")
	stats_parser.set_defaults(func=cmd_stats)

	recommend_parser = subparsers.add_parser(
		"recommend", help="Sugerir o proximo foco de estudo."
	)
	recommend_parser.set_defaults(func=cmd_recommend)

	seed_parser = subparsers.add_parser(
		"seed", help="Adicionar uma lista inicial de tecnologias para explorar."
	)
	seed_parser.set_defaults(func=cmd_seed)

	return parser


def main() -> None:
	parser = build_parser()
	args = parser.parse_args()

	if not hasattr(args, "func"):
		parser.print_help()
		return

	args.func(args)


if __name__ == "__main__":
	main()
