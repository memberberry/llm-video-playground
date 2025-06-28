import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GeminiService {

  constructor(private apiService: ApiService) { }

  getModels(): Observable<{ models: string[] }> {
    return this.apiService.get<{ models: string[] }>('gemini/models');
  }

  requestGeminiFiles(model: string, prompt: string, video_ids: number[]): Observable<any> {
    const body = { model, prompt, video_ids };
    return this.apiService.post('gemini/with_videos', body);
  }

  requestGeminiFilesStruct(model: string, prompt: string, video_ids: number[], response_schema: any): Observable<any> {
    const body = { model, prompt, files: video_ids, response_schema };
    return this.apiService.post('gemini/with_videos_struct', body);
  }
}
