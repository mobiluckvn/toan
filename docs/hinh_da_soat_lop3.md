# Hình đã soát — Tiếng Anh lớp 3

**Soát ngày 18-08-2026, 204 từ.** Đây là lần đầu quyển này được soi hình: cổng
`tienganh_hinh_dung_tu.test.mjs` mở đúng thư mục `ta1` nên lớp 2 và lớp 3 chưa từng
bị nó nhìn ngày nào — xem `docs/tiep_theo_tienganh.md`.

## Ai soát, và soát bằng gì

Soát bởi **Claude (phiên 18-08)**, không phải người. Ghi rõ ra đây vì hai kiểu soát
khác nhau, và bảng này chỉ chứng minh được kiểu thứ nhất:

| soi được | soi bằng gì |
|---|---|
| emoji có vẽ ĐÚNG VẬT không | **tên Unicode chính thức** đặt cạnh nghĩa sách. `🪑` tên là `CHAIR`, đọc ra là thấy — đây là bằng chứng, không phải cảm nhận |
| hai từ có dùng chung một hình không | so theo đúng thứ tự ưu tiên màn hình dùng (`ve` trước, `hinh` sau) |
| hình VẼ TAY có ra đúng vật không | rasterize bằng cairosvg rồi **nhìn ảnh** — năm hình của quyển này đều đã nhìn |
| "không vẽ được" có đúng là không vẽ được không | đọc lý do khai ở `lop3_bu.json` |

Cái bảng này **KHÔNG** thay được người: nó không biết bé tám tuổi nhìn 🛌 có nghĩ ra
"phòng ngủ" hay không. 20 dòng `⚠️ gần đúng` bên dưới là chỗ cần bác quyết.

## Kết quả

| | số từ | |
|---|---|---|
| ✔️ đúng | 107 | tên Unicode khớp nghĩa sách |
| 🚫 không vẽ | 58 | cố ý — từ trừu tượng, tên riêng, lời sai bảo |
| ⚠️ gần đúng | 14 | vẫn dùng được, nhưng lệch một nấc — bác xem lại |
| ✅ đã sửa | 18 | sai hẳn vật, hoặc trùng hình với từ khác |
| ℹ️ ghi chú | 7 | không sai, chỉ là không nhất quán |

### Năm chỗ SAI HẲN VẬT — cùng một dòng họ với `desk` → 🪑 bác bắt ở lớp 1

| từ | nghĩa sách | hình cũ | tên thật của nó |
|---|---|---|---|
| `table` | cái bàn | 🪑 | **CHAIR — cái ghế** |
| `desk` | bàn học | 🪑 | **CHAIR — cái ghế** |
| `eraser` | cục tẩy | 🧽 | **SPONGE — miếng bọt biển rửa bát** |
| `pencil case` | hộp bút | 🧰 | **TOOLBOX — hộp đồ nghề** |
| `swinging` | đu, đánh đu | 🌳 | **DECIDUOUS TREE — cái cây** |

`table` · `desk` · `hair` dùng lại đúng nét vẽ lớp 1 và lớp 2 đã vẽ (cùng một vật thì
phải cùng một hình). `eraser` và `pencil case` vẽ mới. `swinging` chuyển sang "không
vẽ được" vì chưa có emoji nào đúng.

### TÁM NƠI CHỐN — đồ vật đứng thay cho một chỗ (bác chốt vẽ, 18-08)

| từ | hình cũ | tên thật | vấn đề |
|---|---|---|---|
| `library` | 📚 | BOOKS | chồng SÁCH, không phải phòng đọc |
| `art room` | 🖼️ | FRAME WITH PICTURE | bức TRANH treo tường, treo ở đâu cũng được |
| `music room` | 🎹 | MUSICAL KEYBOARD | cái ĐÀN, không phải căn phòng |
| `computer room` | 💻 | PERSONAL COMPUTER | cái LAPTOP, mang đi đâu cũng được |
| `classroom` | 🪑 | CHAIR | cái GHẾ — phòng nào cũng có |
| `gym` | 🏋️ | WEIGHT LIFTER | một NGƯỜI tập tạ |
| `playground` | 🛝 | PLAYGROUND SLIDE | chỉ mỗi CÁI CẦU TRƯỢT |
| `kitchen` | 🍳 | COOKING | cái CHẢO — và trùng hệt `cooking` |

Cả tám hình mới đều dựng trên MỘT KHUNG PHÒNG chung (tường + sàn) rồi mới tới đồ đạc
bên trong — chính cái khung ấy là chỗ phân biệt "cái đàn" với "phòng có cái đàn".

### Sáu chỗ HAI TỪ MỘT HÌNH — phép 2 của cổng, chưa từng chạy cho quyển này

`singer`=`singing` 🎤 · `doctor`=`nurse` 👩‍⚕️ · `bed`=`bedroom` 🛏️ · `gym`=`skipping`
🤸 · `cooking`=`kitchen` 🍳 · `drawing`=`pencil` ✏️. Thêm `come in`=`door`=`room` 🚪 và
`go out`=`walking` 🚶 nữa là tám. Bé học U5 thì 🎤 nghĩa là "hát"; tới U12 vẫn cái
hình ấy lại là "ca sĩ" — với bé chưa đọc chữ, đó là hai bài dạy ngược nhau về cùng
một bức tranh.

Còn ba cặp CỐ Ý để nguyên: `badminton`/`playing badminton`, `basketball`/`playing
basketball`, `kite`/`flying a kite` — danh từ và hoạt động dùng chính vật ấy.

### Bảy chỗ chuyển sang KHÔNG VẼ ĐƯỢC

`open` · `close` · `come in` · `go out` (lời sai bảo trong lớp) · `room` (căn phòng
nói chung) · `driver` (chưa có emoji người lái xe, 🚗 thì trùng `car`) · `swinging`.
Cộng `classroom` — 🧑‍🏫 lại trùng dáng với `teacher`.

⚠ Chúng KHÔNG mất chỗ dạy: video hiện cảnh "dùng trong câu", và câu hỏi bậc 1 tự
chuyển sang bấm CHỮ. Thà trống còn hơn hình sai.

## Bảng 204 từ

| từ | bài | nghĩa sách | hình | tên chuẩn | soát | ghi chú |
|---|---|---|---|---|---|---|
| `one` | B00 | một (1) | 1️⃣ | DIGIT ONE + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `two` | B00 | hai (2) | 2️⃣ | DIGIT TWO + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `three` | B00 | ba (3) | 3️⃣ | DIGIT THREE + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `four` | B00 | bốn (4) | 4️⃣ | DIGIT FOUR + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `five` | B00 | năm (5) | 5️⃣ | DIGIT FIVE + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `six` | B00 | sáu (6) | 6️⃣ | DIGIT SIX + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `seven` | B00 | bảy (7) | 7️⃣ | DIGIT SEVEN + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `eight` | B00 | tám (8) | 8️⃣ | DIGIT EIGHT + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `nine` | B00 | chín (9) | 9️⃣ | DIGIT NINE + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `ten` | B00 | mười (10) | 🔟 | KEYCAP TEN | ✔️ đúng |  |
| `the alphabet (A–Z)` | B00 | bảng chữ cái A đến Z | 🔤 | INPUT SYMBOL FOR LATIN LETTERS | ✔️ đúng |  |
| `hello` | B01 | xin chào | — | *không vẽ* | 🚫 không vẽ | lời chào — diễn bằng CÂU, không vẽ được |
| `hi` | B01 | xin chào | — | *không vẽ* | 🚫 không vẽ | lời chào thân mật |
| `bye` | B01 | chào tạm biệt | — | *không vẽ* | 🚫 không vẽ | lời tạm biệt |
| `goodbye` | B01 | chào tạm biệt | — | *không vẽ* | 🚫 không vẽ | lời tạm biệt trang trọng |
| `fine` | B01 | khoẻ, tốt | — | *không vẽ* | 🚫 không vẽ | “khoẻ” — lời đáp khi được hỏi thăm |
| `how` | B01 | như thế nào | — | *không vẽ* | 🚫 không vẽ | chữ hỏi |
| `I` | B01 | tôi | — | *không vẽ* | 🚫 không vẽ | “mình” |
| `you` | B01 | bạn, các bạn | — | *không vẽ* | 🚫 không vẽ | “bạn” |
| `thank you` | B01 | cảm ơn | — | *không vẽ* | 🚫 không vẽ | lời cảm ơn |
| `Ben` | B01 | bạn Ben | — | *không vẽ* | 🚫 không vẽ |  |
| `Lucy` | B01 | bạn Lucy | — | *không vẽ* | 🚫 không vẽ |  |
| `Mai` | B01 | bạn Mai | — | *không vẽ* | 🚫 không vẽ |  |
| `Minh` | B01 | bạn Minh | — | *không vẽ* | 🚫 không vẽ |  |
| `my` | B02 | của tôi | — | *không vẽ* | 🚫 không vẽ | “của mình” |
| `name` | B02 | tên | — | *không vẽ* | 🚫 không vẽ | “tên” — vẽ ra thì thành tên của MỘT người |
| `what` | B02 | gì | — | *không vẽ* | 🚫 không vẽ | chữ hỏi |
| `your` | B02 | của bạn, của các bạn | — | *không vẽ* | 🚫 không vẽ | “của bạn” |
| `how` | B02 | như thế nào | — | *không vẽ* | 🚫 không vẽ | chữ hỏi |
| `old` | B02 | già; cũ | — | *không vẽ* | 🚫 không vẽ | “cũ, già” |
| `Bill` | B02 | bạn Bill | — | *không vẽ* | 🚫 không vẽ |  |
| `Linh` | B02 | bạn Linh | — | *không vẽ* | 🚫 không vẽ |  |
| `Mary` | B02 | bạn Mary | — | *không vẽ* | 🚫 không vẽ |  |
| `Nam` | B02 | bạn Nam | — | *không vẽ* | 🚫 không vẽ |  |
| `this` | B03 | đây | — | *không vẽ* | 🚫 không vẽ | “cái này” — chỉ vật ở GẦN |
| `that` | B03 | đó, kia | — | *không vẽ* | 🚫 không vẽ | “cái kia” — chỉ vật ở XA |
| `it` | B03 | nó, cái đó, điều đó | — | *không vẽ* | 🚫 không vẽ | “nó” |
| `friend` | B03 | bạn, bạn bè | — | *không vẽ* | 🚫 không vẽ | “bạn” — vẽ ra thành một người cụ thể |
| `teacher` | B03 | giáo viên | 👩‍🏫 | WOMAN + SCHOOL | ℹ️ ghi chú | 👩‍🏫 xuất hiện ở cả U3 và U12 — cùng một từ, nên dùng chung là đúng. |
| `yes` | B03 | vâng | — | *không vẽ* | 🚫 không vẽ | lời đồng ý |
| `no` | B03 | không | — | *không vẽ* | 🚫 không vẽ | lời từ chối |
| `Mr` | B03 | ông | — | *không vẽ* | 🚫 không vẽ | “thầy, ông” — đứng trước tên nam |
| `Ms` | B03 | bà, cô | — | *không vẽ* | 🚫 không vẽ | “cô, bà” — đứng trước tên nữ |
| `Ms Hoa` | B03 | cô Hoa | — | *không vẽ* | 🚫 không vẽ |  |
| `Mr Long` | B03 | thầy Long | — | *không vẽ* | 🚫 không vẽ |  |
| `face` | B04 | mặt | 🙂 | SLIGHTLY SMILING FACE | ⚠️ gần đúng | 🙂 là mặt CƯỜI. Bài dạy "khuôn mặt" — vẫn là cái mặt, nên chưa đổi. |
| `hair` | B04 | tóc | vẽ tay `hair` | mái tóc | ✅ đã sửa | trước là 💇 HAIRCUT — người ĐANG CẮT TÓC. Dùng lại nét vẽ `hair` của lớp 1. |
| `hand` | B04 | bàn tay | ✋ | RAISED HAND | ✔️ đúng |  |
| `ear` | B04 | tai | 👂 | EAR | ✔️ đúng |  |
| `eye` | B04 | mắt | 👁️ | EYE | ✔️ đúng |  |
| `nose` | B04 | mũi | 👃 | NOSE | ✔️ đúng |  |
| `mouth` | B04 | miệng | 👄 | MOUTH | ✔️ đúng |  |
| `touch` | B04 | chạm | 👉 | WHITE RIGHT POINTING BACKHAND INDEX | ⚠️ gần đúng | 👉 là ngón tay CHỈ, không phải động tác chạm. Câu "Touch your nose." thì tạm đọc được. |
| `open` | B04 | mở, há (miệng) | — | *không vẽ* | 🚫 không vẽ | lời sai bảo. 📂 là THƯ MỤC MÁY TÍNH; 📖 thì trùng `reading`. Dạy bằng CÂU. |
| `cooking` | B05 | nấu ăn | 🧑‍🍳 | ADULT + COOKING | ✅ đã sửa | trước 🍳, **trùng hệt `kitchen`**. Nay 🧑‍🍳. |
| `dancing` | B05 | nhảy múa | 💃 | DANCER | ✔️ đúng |  |
| `drawing` | B05 | vẽ | 🖌️ | LOWER LEFT PAINTBRUSH | ✅ đã sửa | trước ✏️, **trùng hệt `pencil`**. Nay 🖌️. |
| `painting` | B05 | tô màu, vẽ tranh | 🎨 | ARTIST PALETTE | ✔️ đúng |  |
| `running` | B05 | chạy | 🏃 | RUNNER | ✔️ đúng |  |
| `singing` | B05 | hát | 🎤 | MICROPHONE | ✔️ đúng |  |
| `swimming` | B05 | bơi | 🏊 | SWIMMER | ✔️ đúng |  |
| `walking` | B05 | đi bộ | 🚶 | PEDESTRIAN | ✔️ đúng |  |
| `school` | B06 | trường học | 🏫 | SCHOOL | ✔️ đúng |  |
| `classroom` | B06 | lớp học | vẽ tay `classroom` | lớp học | ✅ đã sửa | trước là 🪑 **CHAIR — cái ghế**, rồi để trống vì 🧑‍🏫 trùng dáng với `teacher`. Vẽ mới: bảng đen treo tường và hai bộ bàn học. |
| `library` | B06 | thư viện | vẽ tay `library` | thư viện | ✅ đã sửa | trước là 📚 **BOOKS — chồng sách**, đồ vật đứng thay cho căn phòng. Vẽ mới: giá sách hai tầng TRONG khung phòng. |
| `gym` | B06 | nhà thể chất | vẽ tay `gym` | nhà thể chất | ✅ đã sửa | trước 🤸 (trùng `skipping`), rồi 🏋️ (một NGƯỜI tập tạ). Vẽ mới: thang gióng gắn tường và tấm đệm. Cố ý KHÔNG vẽ rổ bóng — `basketball` đã là 🏀. |
| `playground` | B06 | sân chơi | vẽ tay `playground` | sân chơi | ✅ đã sửa | trước là 🛝 — chỉ mỗi CÁI CẦU TRƯỢT. Vẽ mới có khung NGOÀI TRỜI (trời và cỏ) vì sân chơi không phải căn phòng. |
| `art room` | B06 | phòng mĩ thuật | vẽ tay `art_room` | phòng mĩ thuật | ✅ đã sửa | trước là 🖼️ **FRAME WITH PICTURE — bức tranh treo tường**, treo ở đâu cũng được. Vẽ mới: giá vẽ có tranh dở dang và bảng màu. |
| `music room` | B06 | phòng âm nhạc | vẽ tay `music_room` | phòng âm nhạc | ✅ đã sửa | trước là 🎹 **MUSICAL KEYBOARD — cái đàn**, không phải căn phòng. Vẽ mới: đàn phím đứng trong phòng, kèm hai nốt nhạc. |
| `computer room` | B06 | phòng tin học | vẽ tay `computer_room` | phòng tin học | ✅ đã sửa | trước là 💻 **PERSONAL COMPUTER — cái laptop**, mang đi đâu cũng được. Vẽ mới: máy tính đặt trên bàn, có bàn phím và chuột. |
| `our` | B06 | của chúng tôi, của chúng ta | — | *không vẽ* | 🚫 không vẽ | “của chúng mình” |
| `come in` | B07 | đi vào | — | *không vẽ* | 🚫 không vẽ | lời sai bảo. 🚪 là CÁI CỬA, trùng hệt `door`. Dạy bằng CÂU. |
| `go out` | B07 | đi ra | — | *không vẽ* | 🚫 không vẽ | lời sai bảo. 🚶 trùng hệt `walking`. Dạy bằng CÂU. |
| `sit down` | B07 | ngồi xuống | 💺 | SEAT | ⚠️ gần đúng | 💺 là CHỖ NGỒI trên tàu xe, không phải động tác ngồi xuống. Chưa có emoji đúng. |
| `stand up` | B07 | đứng lên | 🧍 | STANDING PERSON | ⚠️ gần đúng | 🧍 là người ĐANG đứng, không thấy động tác đứng LÊN. |
| `close` | B07 | đóng, gấp (sách) | — | *không vẽ* | 🚫 không vẽ | lời sai bảo. 🔒 là cái KHOÁ, không phải gấp sách. Dạy bằng CÂU. |
| `speak` | B07 | nói | 🗣️ | SPEAKING HEAD IN SILHOUETTE | ✔️ đúng |  |
| `please` | B07 | mời, xin mời | — | *không vẽ* | 🚫 không vẽ | tiếng “ạ” — làm câu nhờ thành lịch sự |
| `book` | B08 | quyển sách | 📕 | CLOSED BOOK | ✔️ đúng |  |
| `notebook` | B08 | vở viết | 📓 | NOTEBOOK | ✔️ đúng |  |
| `pen` | B08 | bút | 🖊️ | LOWER LEFT BALLPOINT PEN | ✔️ đúng |  |
| `pencil` | B08 | bút chì | ✏️ | PENCIL | ✔️ đúng |  |
| `pencil case` | B08 | hộp bút | vẽ tay `pencil_case` | hộp bút | ✅ đã sửa | trước là 🧰 **TOOLBOX — hộp đồ nghề**. Vẽ mới: túi có khoá kéo và ba cây bút thò lên. |
| `eraser` | B08 | cục tẩy | vẽ tay `eraser` | cục tẩy | ✅ đã sửa | trước là 🧽 **SPONGE — miếng bọt biển rửa bát**. Vẽ mới: khối trắng đầu xanh, có vụn tẩy rơi. |
| `ruler` | B08 | thước kẻ | 📏 | STRAIGHT RULER | ✔️ đúng |  |
| `school bag` | B08 | cặp sách | 🎒 | SCHOOL SATCHEL | ⚠️ gần đúng | 🎒 đúng cặp sách. |
| `have` | B08 | có | — | *không vẽ* | 🚫 không vẽ | “có” — động từ, không vẽ được |
| `colour` | B09 | màu sắc | — | *không vẽ* | 🚫 không vẽ | “màu sắc” nói chung, không phải một màu cụ thể |
| `black` | B09 | màu đen | ⬛ | BLACK LARGE SQUARE | ✔️ đúng |  |
| `blue` | B09 | màu xanh da trời | 🟦 | LARGE BLUE SQUARE | ✔️ đúng |  |
| `brown` | B09 | màu nâu | 🟫 | LARGE BROWN SQUARE | ✔️ đúng |  |
| `green` | B09 | màu xanh lá cây | 🟩 | LARGE GREEN SQUARE | ✔️ đúng |  |
| `orange` | B09 | màu da cam | 🟧 | LARGE ORANGE SQUARE | ✔️ đúng |  |
| `red` | B09 | màu đỏ | 🟥 | LARGE RED SQUARE | ✔️ đúng |  |
| `white` | B09 | màu trắng | ⬜ | WHITE LARGE SQUARE | ✔️ đúng |  |
| `yellow` | B09 | màu vàng | 🟨 | LARGE YELLOW SQUARE | ✔️ đúng |  |
| `they` | B09 | họ, chúng nó | — | *không vẽ* | 🚫 không vẽ | “các bạn ấy” |
| `break time` | B10 | giờ ra chơi, giờ giải lao | ⏰ | ALARM CLOCK | ⚠️ gần đúng | ⏰ là đồng hồ BÁO THỨC. Giờ ra chơi thì gần, không trúng. |
| `chat` | B10 | nói chuyện | 💬 | SPEECH BALLOON | ✔️ đúng |  |
| `play` | B10 | chơi | 🤾 | HANDBALL | ⚠️ gần đúng | 🤾 là bóng NÉM — một môn cụ thể cho từ "chơi" nói chung. |
| `badminton` | B10 | cầu lông | 🏸 | BADMINTON RACQUET AND SHUTTLECOCK | ℹ️ ghi chú | `badminton` và `playing badminton` chung 🏸 — danh từ và hoạt động dùng chính vật ấy. Chấp nhận được, nhưng vẫn là hai từ một hình. |
| `basketball` | B10 | bóng rổ | 🏀 | BASKETBALL AND HOOP | ℹ️ ghi chú | `basketball` và `playing basketball` chung 🏀 — như trên. |
| `chess` | B10 | cờ | ♟️ | BLACK CHESS PAWN | ⚠️ gần đúng | ♟️ là quân TỐT — một quân cờ đứng thay cho ván cờ. |
| `football` | B10 | bóng đá | ⚽ | SOCCER BALL | ✔️ đúng |  |
| `table tennis` | B10 | bóng bàn | 🏓 | TABLE TENNIS PADDLE AND BALL | ✔️ đúng |  |
| `volleyball` | B10 | bóng chuyền | 🏐 | VOLLEYBALL | ✔️ đúng |  |
| `word puzzle` | B10 | trò chơi ô chữ | 🔠 | INPUT SYMBOL FOR LATIN CAPITAL LETTERS | ⚠️ gần đúng | 🔠 là mấy chữ cái, không phải ô chữ. |
| `father` | B11 | bố, cha | 👨 | MAN | ✔️ đúng |  |
| `mother` | B11 | mẹ | 👩 | WOMAN | ✔️ đúng |  |
| `brother` | B11 | anh trai, em trai | 👦 | BOY | ✔️ đúng |  |
| `sister` | B11 | chị gái, em gái | 👧 | GIRL | ✔️ đúng |  |
| `sure` | B11 | chắc chắn | — | *không vẽ* | 🚫 không vẽ | lời nhận lời |
| `eleven` | B11 | mười một (11) | 1️⃣1️⃣ | DIGIT ONE + COMBINING ENCLOSING KEYCAP + DIGIT ONE + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `twelve` | B11 | mười hai (12) | 1️⃣2️⃣ | DIGIT ONE + COMBINING ENCLOSING KEYCAP + DIGIT TWO + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `thirteen` | B11 | mười ba (13) | 1️⃣3️⃣ | DIGIT ONE + COMBINING ENCLOSING KEYCAP + DIGIT THREE + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `fourteen` | B11 | mười bốn (14) | 1️⃣4️⃣ | DIGIT ONE + COMBINING ENCLOSING KEYCAP + DIGIT FOUR + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `fifteen` | B11 | mười lăm (15) | 1️⃣5️⃣ | DIGIT ONE + COMBINING ENCLOSING KEYCAP + DIGIT FIVE + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `sixteen` | B11 | mười sáu (16) | 1️⃣6️⃣ | DIGIT ONE + COMBINING ENCLOSING KEYCAP + DIGIT SIX + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `seventeen` | B11 | mười bảy (17) | 1️⃣7️⃣ | DIGIT ONE + COMBINING ENCLOSING KEYCAP + DIGIT SEVEN + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `eighteen` | B11 | mười tám (18) | 1️⃣8️⃣ | DIGIT ONE + COMBINING ENCLOSING KEYCAP + DIGIT EIGHT + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `nineteen` | B11 | mười chín (19) | 1️⃣9️⃣ | DIGIT ONE + COMBINING ENCLOSING KEYCAP + DIGIT NINE + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `twenty` | B11 | hai mươi (20) | 2️⃣0️⃣ | DIGIT TWO + COMBINING ENCLOSING KEYCAP + DIGIT ZERO + COMBINING ENCLOSING KEYCAP | ✔️ đúng |  |
| `cook` | B12 | đầu bếp | 👨‍🍳 | MAN + COOKING | ✔️ đúng |  |
| `doctor` | B12 | bác sĩ | 👨‍⚕️ | MAN + STAFF OF AESCULAPIUS | ✅ đã sửa | trước 👩‍⚕️, **trùng hệt `nurse`**. Nay 👨‍⚕️ để hai nghề ra hai hình. |
| `driver` | B12 | tài xế, người lái xe | — | *không vẽ* | 🚫 không vẽ | chưa có emoji NGƯỜI LÁI XE. 🚗 là CÁI XE, trùng hệt `car` của U17. |
| `farmer` | B12 | nông dân | 👨‍🌾 | MAN + EAR OF RICE | ✔️ đúng |  |
| `job` | B12 | nghề nghiệp, công việc | — | *không vẽ* | 🚫 không vẽ | “nghề nghiệp” nói chung |
| `nurse` | B12 | y tá | 👩‍⚕️ | WOMAN + STAFF OF AESCULAPIUS | ⚠️ gần đúng | 👩‍⚕️ và `doctor` 👨‍⚕️ nay khác nhau, nhưng khác bằng GIỚI TÍNH chứ không bằng nghề. |
| `singer` | B12 | ca sĩ | 🧑‍🎤 | ADULT + MICROPHONE | ✅ đã sửa | trước là 🎤, **trùng hệt `singing`**. Nay 🧑‍🎤 — người, không phải cái micro. |
| `teacher` | B12 | giáo viên | 👩‍🏫 | WOMAN + SCHOOL | ℹ️ ghi chú | 👩‍🏫 xuất hiện ở cả U3 và U12 — cùng một từ, nên dùng chung là đúng. |
| `worker` | B12 | công nhân | 👷 | CONSTRUCTION WORKER | ✔️ đúng |  |
| `bathroom` | B13 | phòng tắm | 🛁 | BATHTUB | ✔️ đúng |  |
| `bedroom` | B13 | phòng ngủ | 🛌 | SLEEPING ACCOMMODATION | ✅ đã sửa | trước 🛏️, **trùng hệt `bed`**. Nay 🛌 — người đang ngủ. |
| `kitchen` | B13 | nhà bếp | vẽ tay `kitchen` | nhà bếp | ✅ đã sửa | trước là 🍳 **COOKING — cái chảo**, lại trùng hệt `cooking`. Vẽ mới: bệ bếp hai vòng lửa, nồi bốc hơi, tủ treo. |
| `living room` | B13 | phòng khách | 🛋️ | COUCH AND LAMP | ✔️ đúng |  |
| `chair` | B13 | cái ghế | 🪑 | CHAIR | ✔️ đúng |  |
| `lamp` | B13 | đèn | 💡 | ELECTRIC LIGHT BULB | ✔️ đúng |  |
| `table` | B13 | cái bàn | vẽ tay `table` | cái bàn | ✅ đã sửa | trước là 🪑 **CHAIR — cái GHẾ**. Đúng lỗi bác bắt ở lớp 1, quay lại nguyên văn. Nay dùng nét vẽ `table` lớp 2 đã vẽ. |
| `house` | B13 | ngôi nhà | 🏠 | HOUSE BUILDING | ✔️ đúng |  |
| `here` | B13 | ở đây | — | *không vẽ* | 🚫 không vẽ | “ở đây” |
| `there` | B13 | ở đó, ở kia | — | *không vẽ* | 🚫 không vẽ | “ở kia” |
| `in` | B13 | ở trong | — | *không vẽ* | 🚫 không vẽ | “ở trong” |
| `on` | B13 | ở trên | — | *không vẽ* | 🚫 không vẽ | “ở trên” |
| `bed` | B14 | cái giường | 🛏️ | BED | ✔️ đúng |  |
| `desk` | B14 | bàn học | vẽ tay `desk` | cái bàn học | ✅ đã sửa | trước là 🪑 **CHAIR**. Dùng lại nét vẽ `desk` của lớp 1 — cùng một vật thì phải cùng một hình. |
| `door` | B14 | cái cửa | 🚪 | DOOR | ✔️ đúng |  |
| `window` | B14 | cửa sổ | 🪟 | WINDOW | ✔️ đúng |  |
| `room` | B14 | căn phòng | — | *không vẽ* | 🚫 không vẽ | căn phòng NÓI CHUNG. Vẽ ra là thành một phòng cụ thể; 🚪 trùng `door`. |
| `big` | B14 | to, lớn | — | *không vẽ* | 🚫 không vẽ | “to” |
| `new` | B14 | mới | — | *không vẽ* | 🚫 không vẽ | “mới” |
| `old` | B14 | già; cũ | — | *không vẽ* | 🚫 không vẽ | “cũ, già” |
| `small` | B14 | nhỏ, bé | — | *không vẽ* | 🚫 không vẽ | “nhỏ” |
| `bean` | B15 | đậu | 🫘 | ? | ✔️ đúng |  |
| `bread` | B15 | bánh mì | 🍞 | BREAD | ✔️ đúng |  |
| `chicken` | B15 | thịt gà | 🍗 | POULTRY LEG | ✔️ đúng |  |
| `egg` | B15 | trứng | 🥚 | EGG | ✔️ đúng |  |
| `fish` | B15 | cá | 🐟 | FISH | ✔️ đúng |  |
| `meat` | B15 | thịt | 🥩 | CUT OF MEAT | ✔️ đúng |  |
| `rice` | B15 | cơm, gạo | 🍚 | COOKED RICE | ✔️ đúng |  |
| `juice` | B15 | nước ép | 🧃 | BEVERAGE BOX | ⚠️ gần đúng | 🧃 là HỘP nước, đúng thứ bé uống ở trường. |
| `milk` | B15 | sữa | 🥛 | GLASS OF MILK | ✔️ đúng |  |
| `water` | B15 | nước | 💧 | DROPLET | ⚠️ gần đúng | 💧 là GIỌT nước, không phải cốc nước uống. |
| `bird` | B16 | con chim | 🐦 | BIRD | ✔️ đúng |  |
| `cat` | B16 | con mèo | 🐈 | CAT | ℹ️ ghi chú | lớp 3 dùng 🐈 CẢ CON, lớp 1 dùng 🐱 MẶT MÈO. Cùng một từ, hai quyển hai hình. |
| `dog` | B16 | con chó | 🐕 | DOG | ✔️ đúng |  |
| `goldfish` | B16 | cá vàng | 🐠 | TROPICAL FISH | ✔️ đúng |  |
| `parrot` | B16 | con vẹt | 🦜 | PARROT | ✔️ đúng |  |
| `rabbit` | B16 | con thỏ | 🐇 | RABBIT | ✔️ đúng |  |
| `many` | B16 | nhiều | — | *không vẽ* | 🚫 không vẽ | “nhiều” — đi với vật đếm được |
| `some` | B16 | một vài, một ít | — | *không vẽ* | 🚫 không vẽ | “một ít” |
| `bus` | B17 | xe buýt | 🚌 | BUS | ✔️ đúng |  |
| `car` | B17 | ô tô | 🚗 | AUTOMOBILE | ✔️ đúng |  |
| `kite` | B17 | con diều | 🪁 | KITE | ℹ️ ghi chú | `kite` và `flying a kite` chung 🪁 — như trên. |
| `plane` | B17 | máy bay | ✈️ | AIRPLANE | ✔️ đúng |  |
| `ship` | B17 | con tàu (thuỷ) | 🚢 | SHIP | ✔️ đúng |  |
| `teddy bear` | B17 | gấu bông | 🧸 | TEDDY BEAR | ✔️ đúng |  |
| `toy` | B17 | đồ chơi | — | *không vẽ* | 🚫 không vẽ | “đồ chơi” nói chung |
| `train` | B17 | tàu hoả | 🚆 | TRAIN | ✔️ đúng |  |
| `truck` | B17 | xe tải | 🚚 | DELIVERY TRUCK | ✔️ đúng |  |
| `dancing` | B18 | nhảy múa | 💃 | DANCER | ✔️ đúng |  |
| `drawing a picture` | B18 | vẽ tranh | 🖍️ | LOWER LEFT CRAYON | ✔️ đúng |  |
| `listening to music` | B18 | nghe nhạc | 🎧 | HEADPHONE | ✔️ đúng |  |
| `playing basketball` | B18 | chơi bóng rổ | 🏀 | BASKETBALL AND HOOP | ✔️ đúng |  |
| `reading` | B18 | đọc sách | 📖 | OPEN BOOK | ✔️ đúng |  |
| `singing` | B18 | hát | 🎤 | MICROPHONE | ✔️ đúng |  |
| `watching TV` | B18 | xem ti vi | 📺 | TELEVISION | ✔️ đúng |  |
| `writing` | B18 | viết | ✍️ | WRITING HAND | ✔️ đúng |  |
| `cycling` | B19 | đạp xe | 🚴 | BICYCLIST | ✔️ đúng |  |
| `flying a kite` | B19 | thả diều | 🪁 | KITE | ✔️ đúng |  |
| `painting` | B19 | tô màu, vẽ tranh | 🎨 | ARTIST PALETTE | ✔️ đúng |  |
| `playing badminton` | B19 | chơi cầu lông | 🏸 | BADMINTON RACQUET AND SHUTTLECOCK | ✔️ đúng |  |
| `running` | B19 | chạy | 🏃 | RUNNER | ✔️ đúng |  |
| `skating` | B19 | trượt pa-tanh | ⛸️ | ICE SKATE | ✔️ đúng |  |
| `skipping` | B19 | nhảy dây | 🤸 | PERSON DOING CARTWHEEL | ⚠️ gần đúng | 🤸 là LỘN NHÀO, không phải nhảy dây. Chưa có emoji nhảy dây. |
| `walking` | B19 | đi bộ | 🚶 | PEDESTRIAN | ✔️ đúng |  |
| `elephant` | B20 | con voi | 🐘 | ELEPHANT | ✔️ đúng |  |
| `horse` | B20 | con ngựa | 🐴 | HORSE FACE | ℹ️ ghi chú | dùng emoji MẶT (🐴) trong khi voi · khỉ · hổ · công dùng CẢ CON. Không sai, chỉ là không nhất quán — y hệt chuyện 🐱 của lớp 1. |
| `monkey` | B20 | con khỉ | 🐒 | MONKEY | ✔️ đúng |  |
| `peacock` | B20 | con công | 🦚 | PEACOCK | ✔️ đúng |  |
| `tiger` | B20 | con hổ | 🐅 | TIGER | ✔️ đúng |  |
| `climbing` | B20 | leo trèo | 🧗 | PERSON CLIMBING | ✔️ đúng |  |
| `counting` | B20 | đếm | 🔢 | INPUT SYMBOL FOR NUMBERS | ⚠️ gần đúng | 🔢 là biểu tượng SỐ, không phải động tác đếm. |
| `swinging` | B20 | đu, đánh đu | — | *không vẽ* | 🚫 không vẽ | 🌳 là CÁI CÂY, không phải động tác đu. Chưa có emoji đúng. |
| `dancing` | B20 | nhảy múa | 💃 | DANCER | ✔️ đúng |  |

---

## Còn nợ — chỗ cần NGƯỜI nhìn

1. **14 dòng `⚠️ gần đúng`.** Máy đọc được tên Unicode, không đoán được bé
   nghĩ gì khi nhìn. Nhóm "đồ vật thay cho nơi chốn" đã vẽ hết tám hình. Còn lại là
   những chỗ lệch một nấc về DÁNG (`face` 🙂 mặt cười · `touch` 👉 ngón tay chỉ ·
   `sit down` 💺 chỗ ngồi trên tàu xe · `break time` ⏰ đồng hồ báo thức) và ba chỗ
   chưa có emoji đúng (`skipping` 🤸 lộn nhào · `counting` 🔢 · `word puzzle` 🔠).

   ⚠ `gym` vẽ bằng THANG GIÓNG — cháu đã thử ba kiểu (rổ bóng dễ đọc nhầm thành
   "bóng rổ", người tập tạ là một người chứ không phải căn phòng) và đây là kiểu ít
   lẫn nhất, nhưng nó vẫn có thể đọc ra "cái thang". Bác xem lại giúp.
2. **Hai hình vừa vẽ** (`eraser` · `pencil_case`) cháu đã render ra ảnh và nhìn, nhưng
   bác nên liếc lại một lần trên máy thật.
3. **Lớp 2 vẫn chưa ai soát** — `docs/hinh_da_soat_lop2.md` chưa có. Chạy
   `python3 tools/soat_hinh_tienganh.py --lop 2` là ra bảng.
