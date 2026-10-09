"""
Smoke tests for IDA core (Brain + tools + memory).
Run: python test_v3.py
"""

from brain import CommandParser, Brain
from tools.tools import TOOLS, calculate, run_command, list_notes
from memory_manager import MemoryManager


def test_parser():
    p = CommandParser()
    cases = [
        ("какое сейчас время", "time", None),
        ("погода в Москве", "weather", "москве"),
        ("какая погода в Якутске", "weather", "якутске"),
        ("сегодня хочу выучить python", None, None),
        ("какая дата", "date", None),
        ("посчитай 2+2", "calc", "2+2"),
        ("сколько будет 10/2", "calc", "10/2"),
        ("сколько времени", "time", None),
        ("запомни купить молоко", "note_add", "купить молоко"),
        ("выполни rm -rf /", "run", "rm -rf /"),
        ("что такое IDA", "search", "ida"),
    ]
    failed = 0
    for text, exp_tool, exp_arg in cases:
        tool, arg = p.parse(text)
        ok = tool == exp_tool
        if exp_arg is not None:
            ok = ok and (arg == exp_arg if arg else False)
        if not ok:
            print(f"FAIL parse: {text!r} -> {(tool, arg)} expected {(exp_tool, exp_arg)}")
            failed += 1
        else:
            print(f"OK   parse: {text!r}")
    return failed


def test_tools():
    failed = 0
    r = calculate("2+2*3")
    if "8" not in r:
        print(f"FAIL calc: {r}")
        failed += 1
    else:
        print(f"OK   calc: {r}")

    bad = run_command("rm -rf /")
    if "не разрешена" not in bad:
        print(f"FAIL run whitelist: {bad}")
        failed += 1
    else:
        print(f"OK   run whitelist")

    ok_echo = run_command("echo hello")
    if "hello" not in ok_echo:
        print(f"FAIL echo: {ok_echo}")
        failed += 1
    else:
        print(f"OK   echo")

    notes = list_notes()
    if not isinstance(notes, str):
        print("FAIL notes type")
        failed += 1
    else:
        print("OK   notes")
    return failed


def test_brain_no_key():
    b = Brain({})
    reply = b.generate_response("привет")
    if "IDA" not in reply:
        print(f"FAIL greeting: {reply}")
        return 1
    print(f"OK   greeting: {reply[:60]}...")
    return 0


def test_memory():
    mm = MemoryManager(memory_file="memory/_test_memory.json")
    data = mm.load()
    data["name"] = "TestUser"
    ok = mm.save(data)
    if not ok:
        print("FAIL memory save")
        return 1
    reloaded = mm.load()
    if reloaded.get("name") != "TestUser":
        print(f"FAIL memory load: {reloaded}")
        return 1
    print("OK   memory save/load")
    try:
        import os
        os.remove("memory/_test_memory.json")
    except OSError:
        pass
    return 0


def main():
    print("--- IDA core smoke tests ---")
    failed = 0
    failed += test_parser()
    failed += test_tools()
    failed += test_brain_no_key()
    failed += test_memory()
    print("---")
    if failed:
        print(f"FAILED: {failed}")
        raise SystemExit(1)
    print("ALL PASSED")


if __name__ == "__main__":
    main()
