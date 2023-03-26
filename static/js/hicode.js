ace.require("ace/ext/language_tools");
var editor = ace.edit("editor");
editor.setTheme("ace/theme/textmate");
editor
.session
.setMode("ace/mode/mysql");
editor.setShowPrintMargin(false);

var textarea = $('textarea[name="code_submit"]');
editor
.getSession()
.setValue(textarea.val());
editor
.getSession()
.on('change', function () {
textarea.val(editor.getSession().getValue());
});

