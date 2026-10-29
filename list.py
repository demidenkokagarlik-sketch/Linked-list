import re

# ============================================================
# БЕЗПЕЧНЕ ВВЕДЕННЯ
# ============================================================
def safe_int(prompt, min_val=None, max_val=None):
    while True:
        raw = input(prompt).strip()
        if not re.fullmatch(r"-?\d+", raw):
            print("  ⚠ Введіть ціле число.")
            continue
        v = int(raw)
        if min_val is not None and v < min_val:
            print(f"  ⚠ Має бути >= {min_val}.")
            continue
        if max_val is not None and v > max_val:
            print(f"  ⚠ Має бути <= {max_val}.")
            continue
        return v


def safe_int_list(prompt, elem_min, elem_max, max_len=10000, min_len=0):
    while True:
        raw = input(prompt).strip()
        if raw == "":
            if min_len == 0:
                return []
            print(f"  ⚠ Потрібно щонайменше {min_len} елемент(ів).")
            continue
        parts = [p for p in re.split(r"[,\s]+", raw) if p]
        ok = True
        values = []
        for p in parts:
            if not re.fullmatch(r"-?\d+", p):
                print(f"  ⚠ '{p}' — не ціле число.")
                ok = False
                break
            v = int(p)
            if not (elem_min <= v <= elem_max):
                print(f"  ⚠ {v} поза діапазоном [{elem_min}, {elem_max}].")
                ok = False
                break
            values.append(v)
        if not ok:
            continue
        if not (min_len <= len(values) <= max_len):
            print(f"  ⚠ Кількість елементів має бути в [{min_len}, {max_len}].")
            continue
        return values


# ============================================================
# БАЗОВИЙ ВУЗОЛ ТА ДОПОМІЖНІ ФУНКЦІЇ
# ============================================================
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


def build_list(values):
    dummy = ListNode(0)
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(head):
    out = []
    seen = set()
    while head:
        if id(head) in seen:
            out.append("(cycle)")
            break
        seen.add(id(head))
        out.append(head.val)
        head = head.next
    return out


# ============================================================
# 1. Об'єднати два відсортовані списки
# ============================================================
def merge_two_lists(list1, list2):
    dummy = ListNode(0)
    cur = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            cur.next = list1
            list1 = list1.next
        else:
            cur.next = list2
            list2 = list2.next
        cur = cur.next
    cur.next = list1 if list1 else list2
    return dummy.next


def run_task1():
    list1 = safe_int_list("  list1 (-100..100, 0..50 ел.): ",
                          elem_min=-100, elem_max=100, max_len=50)
    list2 = safe_int_list("  list2 (-100..100, 0..50 ел.): ",
                          elem_min=-100, elem_max=100, max_len=50)
    for name, lst in (("list1", list1), ("list2", list2)):
        if any(lst[i] > lst[i + 1] for i in range(len(lst) - 1)):
            print(f"  ⚠ Увага: {name} не відсортований за неспаданням!")
    result = merge_two_lists(build_list(list1), build_list(list2))
    print(f"  Output: {list_to_array(result)}")


# ============================================================
# 2. Видалити дублікати з відсортованого списку
# ============================================================
def delete_duplicates(head):
    cur = head
    while cur and cur.next:
        if cur.val == cur.next.val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head


def run_task2():
    vals = safe_int_list("  head (-100..100, 0..300 ел.): ",
                         elem_min=-100, elem_max=100, max_len=300)
    if any(vals[i] > vals[i + 1] for i in range(len(vals) - 1)):
        print("  ⚠ Увага: список не відсортований!")
    result = delete_duplicates(build_list(vals))
    print(f"  Output: {list_to_array(result)}")


# ============================================================
# 3. Цикл пов'язаного списку
# ============================================================
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def make_cycle(head, pos):
    """З'єднує хвіст з вузлом під індексом pos (якщо pos >= 0)."""
    if pos < 0 or head is None:
        return head
    nodes = []
    cur = head
    while cur:
        nodes.append(cur)
        cur = cur.next
    if pos >= len(nodes):
        return head
    nodes[-1].next = nodes[pos]
    return head


def run_task3():
    vals = safe_int_list("  head (-100000..100000, 0..10000 ел.): ",
                         elem_min=-100000, elem_max=100000, max_len=10000)
    pos = safe_int(f"  pos (-1 або 0..{max(len(vals)-1, 0)}): ",
                   min_val=-1, max_val=max(len(vals) - 1, 0))
    head = make_cycle(build_list(vals), pos)
    result = has_cycle(head)
    print(f"  Output: {str(result).lower()}")


# ============================================================
# 4. Перевпорядкувати список
# ============================================================
def reorder_list(head):
    if not head or not head.next:
        return head

    # Знаходимо середину
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # Розвертаємо другу половину
    prev = None
    cur = slow.next
    slow.next = None
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt

    # Зливаємо дві половини
    first, second = head, prev
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2

    return head


def run_task4():
    vals = safe_int_list("  head (1..1000, 1..50000 ел.): ",
                         elem_min=1, elem_max=1000, max_len=50000, min_len=1)
    result = reorder_list(build_list(vals))
    print(f"  Output: {list_to_array(result)}")


# ============================================================
# 5. Видалити вузол у зв'язаному списку
# ============================================================
def delete_node(node):
    """Копіює значення наступного вузла у поточний і видаляє наступний."""
    node.val = node.next.val
    node.next = node.next.next


def run_task5():
    print("  (node має бути в списку і не бути останнім)")
    vals = safe_int_list("  head (-1000..1000, 2..1000 ел.): ",
                         elem_min=-1000, elem_max=1000, max_len=1000, min_len=2)
    if len(set(vals)) != len(vals):
        print("  ⚠ Увага: значення мають бути унікальними!")
        return
    node_val = safe_int(f"  node (значення вузла, крім останнього {vals[-1]}): ",
                        min_val=-1000, max_val=1000)
    if node_val not in vals:
        print("  ⚠ Такого вузла немає в списку.")
        return
    if vals[-1] == node_val:
        print("  ⚠ Не можна видаляти останній вузол.")
        return

    head = build_list(vals)
    cur = head
    while cur and cur.val != node_val:
        cur = cur.next
    delete_node(cur)
    print(f"  Output: {list_to_array(head)}")


# ============================================================
# 6. Подвоїти число, представлене зв'язаним списком
# ============================================================
def double_it(head):
    # Розвертаємо, множимо на 2, розвертаємо назад
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt

    carry = 0
    cur = prev
    while cur:
        total = cur.val * 2 + carry
        cur.val = total % 10
        carry = total // 10
        if not cur.next and carry:
            cur.next = ListNode(carry)
            carry = 0
        cur = cur.next

    # Розвертаємо назад
    prev2 = None
    cur = prev
    while cur:
        nxt = cur.next
        cur.next = prev2
        prev2 = cur
        cur = nxt
    return prev2


def run_task6():
    vals = safe_int_list("  head (цифри 0..9, 1..10000 ел.): ",
                         elem_min=0, elem_max=9, max_len=10000, min_len=1)
    if len(vals) > 1 and vals[0] == 0:
        print("  ⚠ Число не може мати початкових нулів (крім '0').")
        return
    result = double_it(build_list(vals))
    print(f"  Output: {list_to_array(result)}")


# ============================================================
# 7. Об'єднати k відсортованих списків
# ============================================================
def merge_k_lists(lists):
    import heapq
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    dummy = ListNode(0)
    cur = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        cur.next = node
        cur = cur.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next


def run_task7():
    print("  (порожній рядок = порожній список)")
    k = safe_int("  k (0..10000): ", min_val=0, max_val=10000)
    lists = []
    total = 0
    for i in range(k):
        while True:
            vals = safe_int_list(f"  lists[{i}] (-10000..10000, 0..500 ел.): ",
                                 elem_min=-10000, elem_max=10000, max_len=500)
            if any(vals[j] > vals[j + 1] for j in range(len(vals) - 1)):
                print("  ⚠ Список має бути відсортований!")
                continue
            if total + len(vals) > 10000:
                print(f"  ⚠ Сумарна кількість вузлів перевищить 10000.")
                continue
            total += len(vals)
            lists.append(build_list(vals))
            break
    result = merge_k_lists(lists)
    print(f"  Output: {list_to_array(result)}")


# ============================================================
# 8. Розвернути вузли в k-групі
# ============================================================
def reverse_k_group(head, k):
    # Перевіряємо, чи є k вузлів
    cur = head
    count = 0
    while cur and count < k:
        cur = cur.next
        count += 1
    if count < k:
        return head

    # Розвертаємо перші k
    prev = None
    cur = head
    for _ in range(k):
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt

    # head тепер — останній вузол розвернутої групи
    head.next = reverse_k_group(cur, k)
    return prev


def run_task8():
    vals = safe_int_list("  head (0..1000, 1..5000 ел.): ",
                         elem_min=0, elem_max=1000, max_len=5000, min_len=1)
    k = safe_int(f"  k (1..{len(vals)}): ", min_val=1, max_val=len(vals))
    result = reverse_k_group(build_list(vals), k)
    print(f"  Output: {list_to_array(result)}")


# ============================================================
# 9. Розділити список
# ============================================================
def partition(head, x):
    less_dummy = ListNode(0)
    ge_dummy = ListNode(0)
    less, ge = less_dummy, ge_dummy
    cur = head
    while cur:
        if cur.val < x:
            less.next = cur
            less = less.next
        else:
            ge.next = cur
            ge = ge.next
        cur = cur.next
    ge.next = None
    less.next = ge_dummy.next
    return less_dummy.next


def run_task9():
    vals = safe_int_list("  head (-100..100, 0..200 ел.): ",
                         elem_min=-100, elem_max=100, max_len=200)
    x = safe_int("  x (-200..200): ", min_val=-200, max_val=200)
    result = partition(build_list(vals), x)
    print(f"  Output: {list_to_array(result)}")


# ============================================================
# ГОЛОВНА ФУНКЦІЯ
# ============================================================
TASKS = {
    1: ("Об'єднати два відсортовані списки", run_task1),
    2: ("Видалити дублікати з відсортованого списку", run_task2),
    3: ("Цикл пов'язаного списку", run_task3),
    4: ("Перевпорядкувати список", run_task4),
    5: ("Видалити вузол у зв'язаному списку", run_task5),
    6: ("Подвоїти число, представлене зв'язаним списком", run_task6),
    7: ("Об'єднати k відсортованих списків", run_task7),
    8: ("Розвернути вузли в k-групі", run_task8),
    9: ("Розділити список", run_task9),
}


def main():
    print("=" * 55)
    print("Доступні задачі (зв'язані списки):")
    for k, (title, _) in TASKS.items():
        print(f"  {k}. {title}")
    print("=" * 55)

    task_num = safe_int("Оберіть задачу (1..9): ", min_val=1, max_val=9)
    title, runner = TASKS[task_num]
    print(f"\n--- Задача {task_num}: {title} ---")
    runner()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nПерервано.")