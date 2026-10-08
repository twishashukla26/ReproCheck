from dataclasses import dataclass


@dataclass
class CheckResult:
    name: str
    status: str
    message: str

    def is_passed(self):
        return self.status == "PASS"

    def is_warning(self):
        return self.status == "WARNING"

    def is_failed(self):
        return self.status == "FAIL"