#include <Servo.h>
Servo servo1;
Servo servo2;

// String entradaSerial = "";         // String para almacenar entrada
// bool entradaCompleta = false;  // Indicar si el String está completo

int pinX = 3;    // pin de conexión PWM al servo
int pinY = 5;
int pulsoMinimo = 580;  // Duración en microsegundos del pulso para girar 0º
int pulsoMaximo = 2500; // Duración en microsegundos del pulso para girar 180º
// int angulo = 0; // Variable para guardar el angulo que deseamos de giro
String entradaSerial = "";         // String para almacenar entrada
bool entradaCompleta = false;  // Indicar si el String está completo


void setup()
{
  servo1.attach(pinX, pulsoMinimo, pulsoMaximo);
  servo2.attach(pinY, pulsoMinimo, pulsoMaximo);
  servo1.write(90);
  servo2.write(45);
  Serial.begin(9600);
}

void loop()
{
    if (!entradaCompleta) return;
    
    int index = entradaSerial.indexOf('@');
    String height = entradaSerial.substring(0, index);
    String width = entradaSerial.substring(index + 1);
    Serial.print(entradaSerial);
    // Mandamos escribir el angulo deseado del giro.
    servo1.write(width.toInt());
    servo2.write(height.toInt());
    entradaSerial = "";
    entradaCompleta = false;
}

void serialEvent() {
  while (Serial.available()) {
    // Obtener bytes de entrada:
    char inChar = (char) Serial.read();
    // Agregar al String de entrada:
    // Para saber si el string está completo, se detendrá al recibir
    if (inChar != '#') {
        entradaSerial += inChar;
    }
    // el caracter de retorno de línea ENTER \n
    if (inChar == '#') {
      entradaCompleta = true;
    }
  }
}
