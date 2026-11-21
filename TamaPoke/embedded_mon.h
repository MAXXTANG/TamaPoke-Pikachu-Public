#pragma once
#include <stdint.h>

// Original PMD SpriteCollab data from the official TamaPoke sprite bundle.
// CC BY-NC; Pokemon characters are Nintendo / Game Freak property.
const uint8_t *embeddedMonData(uint8_t dex, bool shiny, uint32_t &size);
