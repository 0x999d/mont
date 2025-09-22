hello_text = lambda name: (
        f"<b>👋 Привет, {name}!"
        "\n\n📡 С помощью бота вы легко сможете контролировать доступность сайтов: "
        "uptime/downtime, коды HTTP ответов, а также изменение содержимого сайта</b>"
    )

cancell_text = "<b>❌ Действие отменено</b>"

share_url_text = "<b>🔗Хорошо, просто отправь URL для отслеживания</b>"

success_add_url = "<b>🎉 URL успешно добавлен в отслеживаемые!</b>"

already_exist_url = "<b>♻️ Этот URL уже сканируется вами</b>"

timeout_probe_error = "<b>⏳ Timeout error: невозможно добавить недоступный URL</b>"

unexp_probe_error = (
    "<b>🚨 Unexpected error: не получилось проверить URL" 
    "\nПопробуйте еще раз, или убедитесь в его существовании</b>"
)

bad_url_error = (
    "<b>❌ Вы ввели неккоректный URL. "
    "Поддерживаются только HTTP(s), domain.zone & IPv4 URL"
    "\n\n🔹 Например: http://1.1.1.1/hello | https://example.com/hello</b>"
)

url_probe_ok_go_timer = (
    "<b>🕒 Можно выбрать свой интервал в секундах, или оставить стандартный ( <code>60</code> )"
    "\nЧтобы задать интервал, выберите вариант из быстрого меню, или задайте свой"
    "\n\nВ дальнейшем его можно будет изменить</b>"
)

url_added_ok = "<b>🎉 URL успешно добавлен в отслеживаемые!</b>"

start_probe = "<b>⏳ Проверка URL...</b>"

interval_missed_num_error = lambda INTERVALS: (
    f"<b>⚠️ Необходимо написать целое число от {INTERVALS[0]} до {INTERVALS[1]}</b>"
)

no_urls_tracked = "<b>⚠️ У вас нет URL для отслеживания</b>"

choice_url_menu = "<b>🌐 Выберите URL для получения информации</b>"

deleted = "<b>🗑️ Вы перестали отслеживать URL</b>"

already_deleted = "<b>⚠️ URL не отслеживается</b>"

url_change_timer = "<b>🔄 Отправьте новый интервал отслеживания</b>"

interval_change_ok = "<b>✅ Интервал отслеживания изменен</b>"

deleted_url_by_prohibited_detect = lambda url: (
    f"<b>🚫 Отслеживание по {url} остановлено."
    "\nНа запрашиваемый URL добавлены ограничения сканирования</b>"
)

url_down = lambda url: (f"<b>⚠️ Отслеживаемый URL <code>{url}</code> не отвечает</b>")

hash_change_detected = lambda hashes, url: (
    f"<b>🚨 Зафиксирована смена контента: {hashes[0]} -> {hashes[1]}"
    f"\nat <code>{url}</code></b>"
)

url_up = lambda url: (f"<b>✅ Отслеживаемый URL <code>{url}</code> снова отвечает</b>")

requesting_graph = "<b>Создается график...</b>"

url_info = lambda url: (
    f"<b>🖥️ URL {url['url']}"
    f"\n⏱️ Интервал {url['interval']} секунд</b>"
)

url_info = lambda url, graphic_ready: (
    f"<b>{'График еще не доступен' if not graphic_ready else ''}\n\n"
    f"🖥️ URL {url['url']}"
    f"\n⏱️ Интервал {url['interval']} секунд</b>"
)