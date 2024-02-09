import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit{
  
  httpClient = inject(HttpClient);

  data: any = [];
  
  ngOnInit(): void {
    this.fetchData();
  }

  fetchData() {
    this.httpClient.get("http://localhost:8080/produtos")
    .subscribe((data: any) => {
    console.log(data);
    this.data = data;
    });
  }
}
