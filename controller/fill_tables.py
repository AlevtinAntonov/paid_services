from PyQt6 import QtWidgets as qtw
from PyQt6.QtCore import Qt


def fill_table_widget(model, table_widget, non_editable_columns):
    """Обновляет содержимое QTableWidget на основе данных модели."""
    table_widget.setRowCount(0)  # Очищаем существующие данные
    table_widget.setColumnCount(model.columnCount())  # Устанавливаем количество столбцов
    table_widget.verticalHeader().setVisible(False)  # Отключаем отображение номеров строк

    # Заполнение QTableWidget данными из модели
    for row in range(model.rowCount()):
        table_widget.insertRow(row)  # Вставляем новую строку
        for column in range(model.columnCount()):
            item_data = model.data(model.index(row, column))
            item = qtw.QTableWidgetItem()

            if item_data is None:
                item.setText("")  # Если данных нет, оставляем пустым
            else:
                item.setText(str(item_data))  # Преобразуем в строку
                # Если колонка не редактируемая
                if column in non_editable_columns:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Убираем флаг редактирования
                else:
                    if isinstance(item_data, bool):  # Если это логическое значение
                        item.setCheckState(Qt.CheckState.Checked if item_data else Qt.CheckState.Unchecked)
                        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEditable |
                                      Qt.ItemFlag.ItemIsSelectable)
                        item.setText("")
                    else:
                        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable |

                                      ~Qt.ItemFlag.ItemIsUserCheckable)

            table_widget.setItem(row, column, item)
    print('finished filling table')
