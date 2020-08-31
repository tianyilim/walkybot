uint8_t x;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial1.begin(9600);

  Serial.println("Starting serial read test.");
}

void loop() {
  if(Serial1.available()){
    x = Serial1.read();
    Serial.print("Recieved from the Raspi: ");
    Serial.println( x, HEX );
  }

}
