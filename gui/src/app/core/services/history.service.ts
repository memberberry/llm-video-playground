import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { Observable } from 'rxjs';
import { History } from '../models/history.model';

@Injectable({
  providedIn: 'root'
})
export class HistoryService {

  constructor(private apiService: ApiService) { }

  getHistory(): Observable<History[]> {
    return this.apiService.get<History[]>('database/history');
  }

  getHistoryWithVideos(): Observable<any[]> { // Using any[] for now as the backend returns a mixed type
    return this.apiService.get<any[]>('database/history_with_videos');
  }
}
