import { Component, OnInit } from '@angular/core';
import { History } from '../../core/models/history.model';
import { HistoryService } from '../../core/services/history.service';
import { StateService } from '../../shared/services/state.service';
import { MatDialog } from '@angular/material/dialog';
import { HistoryDetailDialogComponent } from '../../shared/components/history-detail-dialog/history-detail-dialog.component';

@Component({
  selector: 'app-history-timeline',
  templateUrl: './history-timeline.component.html',
  styleUrls: ['./history-timeline.component.scss']
})
export class HistoryTimelineComponent implements OnInit {
  history: History[] = [];

  constructor(
    private historyService: HistoryService,
    private stateService: StateService,
    private dialog: MatDialog
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

  openHistoryDetailDialog(hash: string): void {
    this.dialog.open(HistoryDetailDialogComponent, {
      width: '800px',
      data: { hash: hash }
    });
  }
}
