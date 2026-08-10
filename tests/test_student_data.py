import numpy as np
import student_data


def test_delete_student_removes_matching_entries(tmp_path, monkeypatch):
    monkeypatch.setattr(student_data, "DATA_DIR", tmp_path)
    monkeypatch.setattr(student_data, "NAMES_FILE", tmp_path / "names.pkl")
    monkeypatch.setattr(student_data, "FACES_FILE", tmp_path / "faces_data.pkl")

    alice_faces = np.arange(10).reshape(1, 10)
    bob_faces = np.arange(10, 20).reshape(1, 10)

    student_data.save_student_faces("Alice", alice_faces)
    student_data.save_student_faces("Bob", bob_faces)
    student_data.save_student_faces("Alice", alice_faces)

    names = student_data.load_student_names()
    assert names.count("Alice") == 2
    assert names.count("Bob") == 1

    deleted = student_data.delete_student("Alice")

    assert deleted is True
    remaining_names = student_data.load_student_names()
    assert remaining_names == ["Bob"]
