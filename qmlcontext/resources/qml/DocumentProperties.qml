import QtQuick 2.15
import QtQuick.Controls 2.15

Column {

    property alias titleField: titleField
    property alias categoryBox: categoryBox

    TextField {
        id: titleField
        text: document.title
        onTextChanged: document.title = text
    }

    ComboBox {
        id: categoryBox
        model: document.categories
        currentIndex: document.categoryIndex
        onCurrentIndexChanged: document.categoryIndex = currentIndex
    }
}
