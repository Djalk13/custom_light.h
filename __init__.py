#pragma once
#include "esphome.h"
#include <Adafruit_NeoPixel.h>

// === CONFIGURATION ===
#define LED_PIN     5
#define NUM_LEDS    30

// === PARAMÈTRES DE TIMING ===
int strobo_1 = 30;
int strobo_2 = 80;
int strobo_3 = 50;
int strobo_4 = 100;
int freq_1 = 10;
int freq_2 = 30;
int freq_3 = 100;
int freq_pattern_1 = 40;

// === CLASSE PERSONNALISÉE ===
class MyCustomLight : public Component, public light::LightOutput {
  public:
    Adafruit_NeoPixel strip;
    bool is_running = false;

    MyCustomLight() : strip(NUM_LEDS, LED_PIN, NEO_GRBW + NEO_KHZ800) {}

    void setup() override {
      strip.begin();
      strip.show(); // Éteint toutes les LEDs
    }

    light::LightTraits get_traits() override {
      auto traits = light::LightTraits();
      traits.set_supported_color_modes({light::ColorMode::RGB_WHITE});
      return traits;
    }

    // === OUTILS ===
    void setSection(int start, int end, uint32_t color) {
      for (int i = start; i <= end && i < NUM_LEDS; i++) {
        strip.setPixelColor(i, color);
      }
    }

    void clear_strip() {
      strip.clear();
      strip.show();
    }

    // === EFFETS ===
    void rosso() {
      for (int i = 0; i <= 3 && is_running; i++) {
        setSection(0, 9, strip.Color(255, 0, 0, 0));
        strip.show();
        delay(strobo_1);
        clear_strip();
        delay(strobo_1);
      }
    }

    void bianco() {
      for (int i = 0; i <= 3 && is_running; i++) {
        setSection(10, 18, strip.Color(0, 0, 0, 255));
        strip.show();
        delay(strobo_1);
        clear_strip();
        delay(strobo_1);
      }
    }

    void blu() {
      for (int i = 0; i <= 3 && is_running; i++) {
        setSection(19, 29, strip.Color(0, 0, 255, 0));
        strip.show();
        delay(strobo_1);
        clear_strip();
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
        clear_strip();
        delay(strobo_1);
      }
    }

    void mix_rb() {
      for (int i = 0; i <= 3 && is_running; i++) {
        setSection(0, 9, strip.Color(255, 0, 0, 0));
        strip.show();
        delay(strobo_1);
        clear_strip();
        delay(strobo_1);
      }

      for (int i = 0; i <= 3 && is_running; i++) {
        setSection(19, 29, strip.Color(0, 0, 255, 0));
        strip.show();
        delay(strobo_1);
        clear_strip();
        delay(strobo_1);
      }
    }

    void mix_rl_lr() {
      for (int i = 0; i <= 3 && is_running; i++) {
        setSection(0, 4, strip.Color(255, 0, 0, 0));
        setSection(25, 29, strip.Color(0, 0, 255, 0));
        strip.show();
        delay(strobo_1);
        clear_strip();
        delay(strobo_1);
      }

      for (int i = 0; i <= 3 && is_running; i++) {
        setSection(5, 9, strip.Color(255, 0, 0, 0));
        setSection(19, 23, strip.Color(0, 0, 255, 0));
        strip.show();
        delay(strobo_1);
        clear_strip();
        delay(strobo_1);
      }
    }

    void mix_rl_w_lr() {
      for (int i = 0; i <= 3 && is_running; i++) {
        setSection(0, 4, strip.Color(255, 0, 0, 0));
        setSection(10, 18, strip.Color(0, 0, 0, 255));
        setSection(25, 29, strip.Color(0, 0, 255, 0));
        strip.show();
        delay(strobo_1);
        clear_strip();
        delay(strobo_1);
      }

      for (int i = 0; i <= 3 && is_running; i++) {
        setSection(5, 9, strip.Color(255, 0, 0, 0));
        setSection(19, 23, strip.Color(0, 0, 255, 0));
        strip.show();
        delay(strobo_1);
        clear_strip();
        delay(strobo_1);
      }
    }

    void pattern_1() {
      for (int i = 0; i <= 3 && is_running; i++) {
        setSection(0, 4, strip.Color(255, 0, 0, 0));
        setSection(25, 29, strip.Color(0, 0, 255, 0));
        strip.show();
        delay(freq_pattern_1);
        clear_strip();
        delay(freq_pattern_1);
      }

      for (int i = 0; i <= 3 && is_running; i++) {
        setSection(5, 9, strip.Color(255, 0, 0, 0));
        setSection(19, 23, strip.Color(0, 0, 255, 0));
        strip.show();
        delay(freq_pattern_1);
        clear_strip();
        delay(freq_pattern_1);
      }
    }

    void white_blink() {
      for (int i = 0; i <= 3 && is_running; i++) {
        setSection(13, 15, strip.Color(0, 0, 0, 255));
        strip.show();
        delay(freq_pattern_1);
        clear_strip();
        delay(freq_pattern_1);

        setSection(10, 12, strip.Color(0, 0, 0, 255));
        setSection(16, 18, strip.Color(0, 0, 0, 255));
        strip.show();
        delay(freq_pattern_1);
        clear_strip();
        delay(freq_pattern_1);
      }
    }

    // === SÉQUENCE COMPLÈTE ===
    void run_sequence() {
      if (!is_running) return;

      rosso(); delay(strobo_2);
      blu(); delay(strobo_2);
      rosso(); delay(strobo_2);
      blu(); delay(strobo_2);

      mix_rwb(); delay(strobo_2);
      mix_rb(); delay(strobo_2);
      for (int i = 0; i <= 3 && is_running; i++) mix_rl_lr();

      bianco(); delay(strobo_2);
      for (int i = 0; i <= 6 && is_running; i++) mix_rl_w_lr();
      for (int i = 0; i <= 6 && is_running; i++) { rosso(); blu(); }

      for (int i = 0; i <= 6 && is_running; i++) pattern_1();
      white_blink();

      if (is_running) {
        this->set_timeout("loop_again", 10, [this]() { this->run_sequence(); });
      } else {
        clear_strip();
      }
    }

    // === INTÉGRATION AVEC HOME ASSISTANT ===
    void write_state(light::LightState *state) override {
      float brightness;
      state->get_brightness(&brightness);
      bool new_state = brightness > 0.0f;

      if (new_state && !is_running) {
        is_running = true;
        run_sequence();
      } else if (!new_state) {
        is_running = false;
        this->cancel_timeout("loop_again");
        clear_strip();
      }
    }
};
