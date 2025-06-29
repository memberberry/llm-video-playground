import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ApiService } from '../../../core/services/api.service';
import { HistoryWithVideos } from '../../../core/models/history.model';

@Component({
  selector: 'app-history-detail-dialog',
  templateUrl: './history-detail-dialog.component.html',
  styleUrls: ['./history-detail-dialog.component.scss']
})
export class HistoryDetailDialogComponent implements OnInit {
  historyDetail!: HistoryWithVideos;
  jsonOutput: string = '';

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { hash: string },
    private apiService: ApiService
  ) { }

  ngOnInit(): void {
    this.apiService.getHistoryByHash(this.data.hash).subscribe(detail => {
      this.historyDetail = detail;
      if (this.historyDetail.structured_output) {
        this.jsonOutput = JSON.stringify(this.historyDetail.structured_output, null, 2);
      }
    });
  }
}
