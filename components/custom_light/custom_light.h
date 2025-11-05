#pragma once
#include "esphome.h"
#include <Adafruit_NeoPixel.h>

// --- Définition du matériel ---
#define LED_PIN     5
#define NUM_LEDS    30

// --- Paramètres de timing ---
int strobo_1 = 30;
int strobo_2 = 80;
int strobo_3 = 50;
int strobo_4 = 100;
int freq_1 = 10;
int freq_2 = 30;
int freq_3 = 100;
int freq_pattern_1 = 40;

// --- Classe principale ---
class MyCustomLight : public Component, public LightOutput {
 public:
  Adafruit_NeoPixel strip;
  bool is_running = false;

  MyCustomLight() : strip(NUM_LEDS, LED_PIN, NEO_GRBW + NEO_KHZ800) {}

  void setup() override {
    strip.begin();
    strip.show();
  }

  LightTraits get_traits() override {
    auto traits = LightTraits();
    traits.set_supported_color_modes({ColorMode::RGB_WHITE});
    return traits;
  }

  void setSection(int start, int end, uint32_t color) {
    for (int i = start; i <= end; i++) {
      strip.setPixelColor(i, color);
    }
  }

  void rosso() {
    for (int i = 0; i <= 3 && is_running; i++) {
      setSection(0, 9, strip.Color(255, 0, 0, 0));
      strip.show();
      delay(strobo_1);
      if (!is_running) return;
      strip.clear();
      strip.show();
      delay(strobo_1);
    }
  }

  void bianco() {
    for (int i = 0; i <= 3 && is_running; i++) {
      setSection(10, 18, strip.Color(0, 0, 0, 255));
      strip.show();
      delay(strobo_1);
      if (!is_running) return;
      strip.clear();
      strip.show();
      delay(strobo_1);
    }
  }

  void blu() {
    for (int i = 0; i <= 3 && is_running; i++) {
      setSection(19, 29, strip.Color(0, 0, 255, 0));
      strip.show();
      delay(strobo_1);
      if (!is_running) return;
      strip.clear();
      strip.show();
      delay(strobo_1);
    }
  }

  void mix_rwb() {
    for (int i = 0; i <= 6 && is_running; i++) {
      setSection(0, 9, strip.Color(255, 0, 0, 0));
      setSection(10, 18, strip.Color(0, 0, 0, 255));
      setSection(19, 29, strip.Color(0, 0, 255, 0));
      strip.show();
      delay(strobo_1);
      if (!is_running) return;
      strip.clear();
      strip.show();
      delay(strobo_1);
    }
  }

  void run_sequence() {
    if (!is_running) return;
    rosso(); delay(strobo_2); if (!is_running) return;
    blu(); delay(strobo_2); if (!is_running) return;
    mix_rwb(); delay(strobo_2); if (!is_running) return;

    if (is_running) {
      this->set_timeout("loop_again", 10, [this]() { this->run_sequence(); });
    } else {
      this->set_internal_state_to_off();
    }
  }

  void write_state(LightState *state) override {
    float brightness;
    state->get_brightness(&brightness);
    bool new_state = brightness > 0.0f;

    if (new_state && !is_running) {
      is_running = true;
      this->run_sequence();
    } else if (!new_state) {
      is_running = false;
      this->cancel_timeout("loop_again");
      strip.clear();
      strip.show();
      this->set_internal_state_to_off();
    }
  }
};
