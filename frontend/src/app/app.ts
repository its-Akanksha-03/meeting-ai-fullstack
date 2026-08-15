import { Component, ChangeDetectorRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

interface ApiResponse {
  raw_text: string;
  transcript: string;
  summary: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {
  selectedFile: File | null = null;
  loading: boolean = false;
  summary: string = '';
  transcript: string = '';

  constructor(
    private http: HttpClient,
    private cdr: ChangeDetectorRef
  ) {}

  onFileSelected(event: any): void {
    if (event.target.files && event.target.files.length > 0) {
      this.selectedFile = event.target.files[0];
      this.cdr.detectChanges();
    }
  }

  processAudio(): void {
    if (!this.selectedFile) return;

    this.loading = true;
    this.summary = '';
    this.transcript = '';
    this.cdr.detectChanges();

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post<ApiResponse>('http://127.0.0.1:8000/api/process-audio', formData)
      .subscribe({
        next: (res) => {
          this.summary = res.summary;
          this.transcript = res.transcript;
          this.loading = false;
          this.cdr.detectChanges();
        },
        error: (err) => {
          console.error(err);
          this.loading = false;
          this.cdr.detectChanges();
          alert('Error processing audio. Make sure the backend terminal is running.');
        }
      });
  }
}