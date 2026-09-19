from dataclasses import dataclass, field


@dataclass
class TokenVault:
    _mapping: dict[str, str] = field(default_factory=dict)

    def store(self, token: str, value: str) -> None:
        self._mapping[token] = value

    def store_many(self, mapping: dict[str, str]) -> None:
        for token, value in mapping.items():
            self.store(token, value)

    def restore(self, text: str) -> str:
        restored = text

        for token, value in self._mapping.items():
            restored = restored.replace(token, value)

        return restored

    def clear(self) -> None:
        self._mapping.clear()

    def __len__(self) -> int:
        return len(self._mapping)