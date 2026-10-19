import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

export interface PredictionResponse {
  prediction: number;
  label: string;
  delay_probability: number;
  probabilities: number[];
  classes: number[];
  disclaimer: string;
}

@Injectable({ providedIn: 'root' })
export class PredictionService {
  private http = inject(HttpClient);

  predict(payload: Record<string, string | number>) {
    return this.http.post<PredictionResponse>('/api/predict', payload);
  }
}