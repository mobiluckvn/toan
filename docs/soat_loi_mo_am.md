# SỔ SOÁT · LỜI MỞ "BA TỪ CÙNG ÂM" TRONG VIDEO TỪ MỚI

Soát ngày **18-08-2026**, sau khi bác bắt:

> "Mình thấy từ lớp 2 đến lớp 3 là nhiều từ mới không có trong nhóm âm. Nhưng
> video dạy từ mới bạn vẫn mô típ là hãy nghe 03 từ thấy giống nhau gì không?
> Giống nhau âm ... Hoàn toàn sai. Bạn hãy review lại tất cả các video về học từ
> mới từ lớp 2 đến lớp 3 để xem video nào sai thì làm lại và bỏ cái kiểu mở màn
> đó đi nhé"

## Chỗ hỏng nằm ở đâu

`tools/sinh_bai_tienganh.py` dựng câu K2 bằng cách lấy **ba từ đầu tiên** của unit
rồi khẳng định luôn là chúng bắt đầu giống nhau — không hỏi lại lấy một lần:

```python
ba = " · ".join(t["tu"] for t in tu[:3])
"text": f"Nghe ba từ này: {ba}. Con có nghe thấy chúng bắt đầu giống nhau không?"
```

Câu ấy đi vào **hai chỗ**: cảnh `chu_cai` của video từ mới (bé nghe), và mục K2 ở
Góc bố mẹ (người lớn đọc).

Tiền đề của nó chỉ đúng với **lớp 1**, quyển xếp bài THEO CHỮ CÁI. Từ lớp 2 sách
xếp theo CHỦ ĐỀ, nên tiền đề sụp hẳn — mà câu vẫn được sinh ra y nguyên.

## Đếm được bao nhiêu

| Quyển | Sai | Tổng | |
|---|---|---|---|
| Lớp 1 | 6 | 16 | quyển dạy phonics, phần lớn còn đúng |
| Lớp 2 | 8 | 16 | |
| Lớp 3 | **21** | **21** | không unit nào đúng |

Ba ví dụ tiêu biểu:

* `box · fox · ox` — chữ **x** nằm ở CUỐI từ, không phải đầu
* `bird · cat · dog` — chẳng có âm nào chung
* `cooking · dancing · drawing` — bài khai chữ **p**

## Vì sao không cổng nào bắt được

Mọi thứ **đo được** đều đúng: câu đúng ngữ pháp, clip tiếng có đủ, video dựng ra
bình thường, độ dài trong ngưỡng. Chỉ NGHE mới biết nó nói sai. Cùng họ với
[[hinh-trong-video-phai-khop-loi-doc]] — cổng đếm được nhưng không hiểu nghĩa.

## Nay làm gì

1. `am_dau_khop()` trong `sinh_bai_tienganh.py` **hỏi lại** trước khi sinh: ba từ
   ấy có thật sự bắt đầu bằng chữ bài khai không.
2. Không đúng thì **K2 không tồn tại**. `kich_ban.py` vốn đã viết
   `if dau_tien and "K2" in K` — nên cảnh `chu_cai` tự biến mất, không phải sửa
   thêm dòng nào. Một chỗ khai, hai nơi nghe theo.
3. K1 thay bằng câu đúng và có ích: *"Hôm nay chúng mình học 8 từ mới — Sở thích
   của mình."*
4. Cổng mới ở `tienganh_bai.test.mjs` §4D soi **hai chiều**: bài nói sai thì đỏ,
   mà bài có âm chung thật lại bỏ mất phần dạy cũng đỏ. Đã đảo chiều thử: nhét lại
   K2 vào U16 lớp 3 → cổng đỏ đúng chỗ.

## Bảng chi tiết

### LỚP 1

| Unit | Chữ bài khai | Ba từ đầu | Lời mở cũ | Nay |
|---|---|---|---|---|
| U01 | `b` | ball · bike · book | đúng | giữ |
| U02 | `c` | cake · car · cat | đúng | giữ |
| U03 | `a` | apple · bag · can | **SAI** | bỏ |
| U04 | `d` | desk · dog · door | đúng | giữ |
| U05 | `i` | chicken · chips · fish | **SAI** | bỏ |
| U06 | `e` | bell · pen · pencil | **SAI** | bỏ |
| U07 | `g` | garden · gate · girl | đúng | giữ |
| U08 | `h` | hair · hand · head | đúng | giữ |
| U09 | `o` | clocks · locks · mops | **SAI** | bỏ |
| U10 | `m` | mango · monkey · mother | đúng | giữ |
| U11 | `u` | bus · run · sun | **SAI** | bỏ |
| U12 | `l` | lake · leaf · lemons | đúng | giữ |
| U13 | `n` | bananas · noodles · nuts | **SAI** | bỏ |
| U14 | `t` | teddy bear · tiger · top | đúng | giữ |
| U15 | `f` | face · father · foot | đúng | giữ |
| U16 | `w` | wash · water · window | đúng | giữ |

### LỚP 2

| Unit | Chữ bài khai | Ba từ đầu | Lời mở cũ | Nay |
|---|---|---|---|---|
| U01 | `p` | pasta · popcorn · pizza | đúng | giữ |
| U02 | `k` | kite · bike · kitten | **SAI** | bỏ |
| U03 | `s` | sail · sand · sea | đúng | giữ |
| U04 | `r` | rainbow · river · road | đúng | giữ |
| U05 | `q` | question · square · quiz | **SAI** | bỏ |
| U06 | `x` | box · fox · ox | **SAI** | bỏ |
| U07 | `j` | juice · jelly · jam | đúng | giữ |
| U08 | `v` | village · van · volleyball | đúng | giữ |
| U09 | `y` | yogurt · yam · yo-yo | đúng | giữ |
| U10 | `z` | zoo · zebu · zebra | đúng | giữ |
| U11 | `i` | slide · ride · drive | **SAI** | bỏ |
| U12 | `a` | grape · cake · table | **SAI** | bỏ |
| U13 | `n` | eleven · twelve · thirteen | **SAI** | bỏ |
| U14 | `er` | brother · sister · grandmother | **SAI** | bỏ |
| U15 | `sh` | shirt · shoes · shorts | đúng | giữ |
| U16 | `t` | tent · teapot · blanket | **SAI** | bỏ |

### LỚP 3

| Unit | Chữ bài khai | Ba từ đầu | Lời mở cũ | Nay |
|---|---|---|---|---|
| U00 | `—` | one · two · three | **SAI** | bỏ |
| U01 | `h` | hello · hi · bye | **SAI** | bỏ |
| U02 | `m` | my · name · what | **SAI** | bỏ |
| U03 | `th` | this · that · it | **SAI** | bỏ |
| U04 | `h` | face · hair · hand | **SAI** | bỏ |
| U05 | `p` | cooking · dancing · drawing | **SAI** | bỏ |
| U06 | `pl` | school · classroom · library | **SAI** | bỏ |
| U07 | `sp` | come in · go out · sit down | **SAI** | bỏ |
| U08 | `b` | book · notebook · pen | **SAI** | bỏ |
| U09 | `bl` | colour · black · blue | **SAI** | bỏ |
| U10 | `f` | break time · chat · play | **SAI** | bỏ |
| U11 | `o` | father · mother · brother | **SAI** | bỏ |
| U12 | `er` | cook · doctor · driver | **SAI** | bỏ |
| U13 | `ou` | bathroom · bedroom · kitchen | **SAI** | bỏ |
| U14 | `o` | bed · desk · door | **SAI** | bỏ |
| U15 | `ea` | bean · bread · chicken | **SAI** | bỏ |
| U16 | `o` | bird · cat · dog | **SAI** | bỏ |
| U17 | `i` | bus · car · kite | **SAI** | bỏ |
| U18 | `n` | dancing · drawing a picture · listening to music | **SAI** | bỏ |
| U19 | `pl` | cycling · flying a kite · painting | **SAI** | bỏ |
| U20 | `a` | elephant · horse · monkey | **SAI** | bỏ |
