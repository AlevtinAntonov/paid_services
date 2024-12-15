from controller.fill_tables import fill_table_widget


def setup_tables_views(model, table_widget, filter_condition=None, filter_value=None, columns=None, slot=None):
    table_widget.itemChanged.disconnect()  # Отключаем сигнал изменения
    model.select()  # Выполняем выборку

    if filter_condition and filter_value is not None:
        model.setFilter(f"{filter_condition} = {filter_value}")
        model.select()  # Выполняем выборку с фильтром

    # Проверка на ошибки после выполнения запроса
    if model.lastError().isValid():
        print("Ошибка запроса:", model.lastError().text())
        return

    fill_table_widget(model, table_widget, columns)

    if slot:  # Если слот указан, подключаем его
        table_widget.itemChanged.connect(slot)