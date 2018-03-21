function IsNumeric(input)
{
   return (input - 0) == input && input.length > 0;
}

if(!String.prototype.startsWith){
    String.prototype.startsWith = function (str) {
        return !this.indexOf(str);
    };
}

$(document).ready(function(){
    $('#errores').hide();
    $('#tweets').linedtextarea();

    var re = /(https?:\/\/[a-zA-Z0-9$-_@.&+!*(),]+(?:.png|.jpg|.jpeg|.PNG|.JPG|.JPEG))/;

    var date = new Date();
    $('#inicio').val(date.getFullYear() + "-" + (date.getMonth()+1) + "-" + (date.getDate()));

    $('#submit').click(function(){
        var lines = $('#tweets').val().split("\n");
        $('#listaerrores').empty();
        var error = false;
        for (var line in lines){
            if (lines[line].startsWith("-wait")){
                var wait = lines[line].split(" ");
                if (wait.length != 2) {
                    $('#listaerrores').append($('<li>' + "-wait incocrrecto (argumentos invalidos): linea " + (parseInt(line)+1) + "</li>"));
                    error = true;
                }
                else if (!IsNumeric(wait[1])){
                    $('#listaerrores').append($('<li>' + "-wait incorrecto (argumento no es un numero): linea " + (parseInt(line)+1) + "</li>"));
                    error = true;
                }
                
            }
            else if (lines[line].length > 279){
                $('#listaerrores').append($('<li>' + "La linea " + (line+1)  + " es de mas de 279 caracteres" + "</li>"));
                error = true;
            }
        }
        if (error){
            $('#errores').show();
            return false;
        }
        return true;
    });
});
