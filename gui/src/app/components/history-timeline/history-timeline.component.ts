import { Component, OnInit } from '@angular/core';
import { History } from '../../core/models/history.model';
import { HistoryService } from '../../core/services/history.service';
import { StateService } from '../../shared/services/state.service';

@Component({
  selector: 'app-history-timeline',
  templateUrl: './history-timeline.component.html',
  styleUrls: ['./history-timeline.component.scss']
})
export class HistoryTimelineComponent implements OnInit {
  history: History[] = [];

  constructor(
    private historyService: HistoryService,
    private stateService: StateService
  ) { }

  ngOnInit(): void {
    this.loadHistory();
    this.stateService.refreshHistory$.subscribe(() => {
      this.loadHistory();
    });
  }

  loadHistory(): void {
    this.historyService.getHistory().subscribe(history => {
      this.history = history;
    });
  }
}
