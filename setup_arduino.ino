int led_verde = 7; // LED verde na porta 7
int led_vermelho = 2; // LED vermelho na porta 2

void setup() {
  pinMode(led_verde, OUTPUT);
  pinMode(led_vermelho, OUTPUT);
  Serial.begin(9600); // Inicializar comunicação serial
}

void loop() {
  if (Serial.available()) {
    char comando = Serial.read();
    if (comando == 'G') {
      digitalWrite(led_verde, HIGH);  
      digitalWrite(led_vermelho, LOW); 
    } 
    else if (comando == 'R') {
      digitalWrite(led_vermelho, HIGH);  
      digitalWrite(led_verde, LOW);      
    } 
    else if (comando == 'O') {
      digitalWrite(led_vermelho, LOW); 
      digitalWrite(led_verde, LOW);
    }
  }
}
