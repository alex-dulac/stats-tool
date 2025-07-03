<script setup lang="ts">
import {computed, ref} from "vue";
import apiClient from "@api/apiClient.ts";
import * as Plot from "@observablehq/plot";
import * as d3 from "d3";
import { useSessionStore } from "@library/store.ts";
import SeasonFilter from "@components/content/SeasonFilter.vue";
import LoadingCircle from "@components/LoadingCircle.vue";

const sessionStore = useSessionStore();
const data = ref();
const loading = ref(true);
const chartContainer = ref();
const items = computed(() => data.value?.data || []);

const fetchDataAndRefreshPlot = async (season: number) => {
  loading.value = true;

  const response = await apiClient.getPerGameConsistency(season);
  data.value = response.data;
  refreshRadarChart();

  loading.value = false;
};

const refreshRadarChart = () => {
  // example as a guide: https://observablehq.com/@observablehq/plot-radar-chart
  // rather complex --- improve me!
  const metrics = ["goalsPerGame", "assistsPerGame", "shotsPerGame", "toiPerGame"];

  const maxValues: Record<string, number> = {};
  metrics.forEach(metric => {
    maxValues[metric] = Math.max(...items.value.map((d: any) => d[metric] || 0));
  });

  const points = items.value.flatMap((player: any) =>
      metrics.map(metric => ({
        name: player.playerName,
        team: player.team,
        key: metric,
        value: (player[metric] || 0) / maxValues[metric], // Normalize to 0-1
        rawValue: player[metric] || 0
      }))
  );

  const longitude = d3.scalePoint()
      .domain(metrics)
      .range([180, -180])
      .padding(0.1);

  const formatMetricName = (metric: string) =>
      metric.replace(/([A-Z])/g, ' $1')
          .replace(/^./, str => str.toUpperCase())
          .replace('Per Game', '/Game');

  const plot = Plot.plot({
    width: 1000,
    height: 1000,
    margin: 50,
    projection: {
      type: "azimuthal-equidistant",
      rotate: [0, -90],
      domain: d3.geoCircle().center([0, 90]).radius(1.125)() // large radius for labels
    },
    marks: [
      // grey discs
      Plot.geo([1.0, 0.8, 0.6, 0.4, 0.2], {
        geometry: (r) => d3.geoCircle().center([0, 90]).radius(r)(),
        stroke: sessionStore.getTheme === 'dark' ? "#555" : "#ddd",
        fill: sessionStore.getTheme === 'dark' ? "#333" : "#f8f8f8",
        strokeOpacity: 0.5,
        fillOpacity: 0.05,
        strokeWidth: 1
      }),

      // axis lines
      Plot.link(longitude.domain(), {
        x1: longitude,
        y1: 90 - 1.07,
        x2: 0,
        y2: 90,
        stroke: sessionStore.getTheme === 'dark' ? "#666" : "#ccc",
        strokeOpacity: 0.7,
        strokeWidth: 1.5
      }),

      // tick labels
      Plot.text([0.2, 0.4, 0.6, 0.8, 1.0], {
        x: 180,
        y: (d) => 90 - d,
        dx: 4,
        textAnchor: "start",
        text: (d) => `${Math.round(100 * d)}%`,
        fill: sessionStore.getTheme === 'dark' ? "#888" : "#666",
        stroke: sessionStore.getTheme === 'dark' ? "#000" : "#fff",
        strokeWidth: 2,
        fontSize: 10
      }),

      // Metric labels around the perimeter
      Plot.text(longitude.domain(), {
        x: longitude,
        y: 90 - 1.07,
        text: formatMetricName,
        fill: sessionStore.getTheme === 'dark' ? "#fff" : "#000",
        stroke: sessionStore.getTheme === 'dark' ? "#000" : "#fff",
        strokeWidth: 2,
        fontSize: 12,
        fontWeight: "bold",
        textAnchor: "middle",
        lineWidth: 8
      }),

      // player areas
      Plot.area(points, {
        x1: ({ key }) => longitude(key),
        y1: ({ value }) => 90 - value,
        x2: 0,
        y2: 90,
        fill: "name",
        stroke: "name",
        strokeWidth: 2,
        fillOpacity: 0.15,
        strokeOpacity: 0.8,
        curve: "cardinal-closed"
      }),

      // data points
      Plot.dot(points, {
        x: ({ key }) => longitude(key),
        y: ({ value }) => 90 - value,
        fill: "name",
        stroke: sessionStore.getTheme === 'dark' ? "#000" : "#fff",
        strokeWidth: 2,
        r: 4,
        title: (d) => `${d.name} (${d.team})\n${formatMetricName(d.key)}: ${d.rawValue.toFixed(2)}`,
        tip: {
          fill: sessionStore.getTheme === 'dark' ? "#333" : "#fff",
          textColor: sessionStore.getTheme === 'dark' ? "#fff" : "#000"
        }
      }),
    ]
  });

  chartContainer.value.innerHTML = '';
  chartContainer.value.appendChild(plot);

  // Hover fills being handled a little differently than the linked example
  const fillOpacity = sessionStore.getTheme === 'dark' ? '0.1' : '0.15';
  const hoverOpacity = sessionStore.getTheme === 'dark' ? '0.25' : '0.3';
  const fadeOpacity = sessionStore.getTheme === 'dark' ? '0.05' : '0.08';

  const style = document.createElement('style');
  style.textContent = `
    .chart g[aria-label=area] path {
      fill-opacity: ${fillOpacity};
      transition: fill-opacity 0.2s ease;
    }
    .chart g[aria-label=area]:hover path:not(:hover) {
      fill-opacity: ${fadeOpacity};
      transition: fill-opacity 0.2s ease;
    }
    .chart g[aria-label=area] path:hover {
      fill-opacity: ${hoverOpacity};
      transition: fill-opacity 0.2s ease;
    }
  `;

  const existingStyle = chartContainer.value.querySelector('style');
  if (existingStyle) {
    existingStyle.remove();
  }

  chartContainer.value.appendChild(style);
};
</script>

<template>
  <div class="chart-container">
    <SeasonFilter :onChange="fetchDataAndRefreshPlot" />
    <LoadingCircle v-if="loading" />
    <div ref="chartContainer" class="chart" />
  </div>
</template>
