import { Component, inject, signal } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { FEATURES, SAMPLE } from './feature-schema';
import {
  PredictionService,
  PredictionResponse,
} from './prediction.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, DecimalPipe],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  readonly fields = FEATURES;
  readonly deployedStatic =
    !['localhost', '127.0.0.1'].includes(window.location.hostname);

  values: Record<string, string | number | null> = this.emptyValues();
  loading = signal(false);
  error = signal('');
  result = signal<PredictionResponse | null>(null);

  private api = inject(PredictionService);

  private emptyValues(): Record<string, string | number | null> {
    return Object.fromEntries(FEATURES.map(field => [field.name, null]));
  }

  loadSample() {
    this.values = { ...SAMPLE };
    this.error.set('');
    this.result.set(null);
  }

  clear() {
    this.values = this.emptyValues();
    this.error.set('');
    this.result.set(null);
  }

  submit() {
    if (this.loading()) return;

    this.error.set('');
    this.result.set(null);

    if (this.deployedStatic) {
      this.error.set('Predictions require Flask and Angular running locally.');
      return;
    }

    const payload: Record<string, string | number> = {};

    for (const field of this.fields) {
      const value = this.values[field.name];

      if (
        value === null ||
        value === undefined ||
        (typeof value === 'string' && !value.trim())
      ) {
        this.error.set(`Enter ${field.label}.`);
        return;
      }

      if (field.kind === 'number') {
        const number = Number(value);

        if (!Number.isFinite(number)) {
          this.error.set(`${field.label} must be a valid number.`);
          return;
        }

        payload[field.name] = number;
      } else {
        payload[field.name] = String(value);
      }
    }

    this.loading.set(true);

    this.api.predict(payload).subscribe({
      next: response => {
        this.result.set(response);
        this.loading.set(false);
      },
      error: err => {
        this.error.set(
          err.error?.error || 'Cannot reach the API. Check the Flask terminal.'
        );
        this.loading.set(false);
      },
    });
  }
}