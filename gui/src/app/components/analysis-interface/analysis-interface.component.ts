import { Component, OnInit } from '@angular/core';
import { GeminiService } from '../../core/services/gemini.service';
import { StateService } from '../../shared/services/state.service';
import { Video } from '../../core/models/video.model';

@Component({
  selector: 'app-analysis-interface',
  templateUrl: './analysis-interface.component.html',
  styleUrls: ['./analysis-interface.component.scss']
})
export class AnalysisInterfaceComponent implements OnInit {
  models: string[] = [];
  selectedModel: string = 'gemini-1.5-pro';
  outputType: 'structured' | 'text' = 'structured';
  prompt: string = '';
  response: any = null;
  selectedVideos: Video[] = [];

  constructor(
    private geminiService: GeminiService,
    private stateService: StateService
  ) { }

  ngOnInit(): void {
    this.geminiService.getModels().subscribe(res => {
      this.models = res.models;
    });
    this.stateService.selectedVideos$.subscribe(videos => {
      this.selectedVideos = videos;
    });
  }

  sendRequest(): void {
    const video_ids = this.selectedVideos.map(v => v.id);
    if (this.outputType === 'structured') {
      // A default schema for demonstration. This should be dynamic in a real app.
      const schema = {
        type: 'OBJECT',
        properties: {
          summary: { type: 'STRING' },
          key_topics: { type: 'ARRAY', items: { type: 'STRING' } }
        },
        required: ['summary', 'key_topics']
      };
      this.geminiService.requestGeminiFilesStruct(this.selectedModel, this.prompt, video_ids, schema)
        .subscribe(res => {
          this.response = res.parsed;
          this.stateService.triggerHistoryRefresh();
        });
    } else {
      this.geminiService.requestGeminiFiles(this.selectedModel, this.prompt, video_ids)
        .subscribe(res => {
          this.response = res.text;
          this.stateService.triggerHistoryRefresh();
        });
    }
  }
}
