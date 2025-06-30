import { Component, OnInit } from '@angular/core';
import { GeminiService } from '../../core/services/gemini.service';
import { StateService } from '../../shared/services/state.service';
import { Video } from '../../core/models/video.model';
import { finalize, catchError } from 'rxjs/operators';
import { of } from 'rxjs';

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
  jsonSchemaInput: string = JSON.stringify({
    type: 'OBJECT',
    properties: {
      video_highlights: {
        type: 'ARRAY',
        description: 'A list of video highlights',
        items: {
          type: 'OBJECT',
          properties: {
            start: { type: 'NUMBER', description: 'Start time of the highlight in seconds' },
            end: { type: 'NUMBER', description: 'End time of the highlight in seconds' },
            summary: { type: 'STRING', description: 'A brief summary of the highlight' },
            title: { type: 'STRING', description: 'A title for the highlight' }
          },
          required: ['start', 'end', 'summary', 'title']
        }
      }
    },
    required: ['video_highlights']
  }, null, 2);
  jsonSchemaError: string = '';
  response: any = null;
  selectedVideos: Video[] = [];
  loadingGemini: boolean = false;
  geminiError: string | null = null;

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

  formatJsonInput(): void {
    try {
      const parsed = JSON.parse(this.jsonSchemaInput);
      this.jsonSchemaInput = JSON.stringify(parsed, null, 2);
      this.jsonSchemaError = '';
    } catch (e: any) {
      this.jsonSchemaError = 'Invalid JSON format: ' + e.message;
    }
  }

  sendRequest(): void {
    this.jsonSchemaError = ''; // Clear previous errors
    this.geminiError = null; // Clear previous errors
    this.loadingGemini = true; // Set loading to true

    const video_ids = this.selectedVideos.map(v => v.id);
    if (this.outputType === 'structured') {
      let schema: any;
      try {
        schema = JSON.parse(this.jsonSchemaInput);
      } catch (e: any) {
        this.jsonSchemaError = 'Invalid JSON schema: ' + e.message;
        this.loadingGemini = false; // Set loading to false on error
        return; // Stop execution if JSON is invalid
      }

      this.geminiService.requestGeminiFilesStruct(this.selectedModel, this.prompt, video_ids, schema).pipe(
        finalize(() => this.loadingGemini = false),
        catchError(error => {
          this.geminiError = 'Failed to get structured output from Gemini.';
          console.error('Gemini structured request error:', error);
          return of(null);
        })
      ).subscribe(res => {
        this.response = res?.parsed;
        this.stateService.triggerHistoryRefresh();
      });
    } else {
      this.geminiService.requestGeminiFiles(this.selectedModel, this.prompt, video_ids).pipe(
        finalize(() => this.loadingGemini = false),
        catchError(error => {
          this.geminiError = 'Failed to get text output from Gemini.';
          console.error('Gemini text request error:', error);
          return of(null);
        })
      ).subscribe(res => {
        this.response = res?.text;
        this.stateService.triggerHistoryRefresh();
      });
    }
  }
}
