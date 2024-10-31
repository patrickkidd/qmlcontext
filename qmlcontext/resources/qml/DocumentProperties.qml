import QtQuick 2.15
import QtQuick.Controls 2.15

Column {

    property alias titleField: titleField
    property alias categoryBox: categoryBox

    Connections {
        target: document
        function onTitleChanged() {
            titleField.text = document.title
        }
        function onCategoryIndexChanged() {
            categoryBox.currentIndex = document.categoryIndex
        }
    }

    Keys.onPressed: {
        console.log("Key pressed: " + event.key)
    }

    TextField {
        id: titleField
        onActiveFocusChanged: {
            if (activeFocus) {
                print("TextField gained focus")
            } else {
                print("TextField lost focus")
            }
        }
        onTextChanged: {
            print('onTextChanged: ' + text)
            if(document.title != text) {
                document.title = text
            }
        }
    }

    ComboBox {
        id: categoryBox
        model: document.categories
        onCurrentIndexChanged: {
            if(document.categoryIndex != currentIndex)
                document.categoryIndex = currentIndex
        }
        onModelChanged: {
            document.categoryIndex = -1
        }
    }
}
