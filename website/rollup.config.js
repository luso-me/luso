import svelte from 'rollup-plugin-svelte';
import commonjs from '@rollup/plugin-commonjs';
import resolve from '@rollup/plugin-node-resolve';
import livereload from 'rollup-plugin-livereload';
import {terser} from 'rollup-plugin-terser';
import sveltePreprocess from 'svelte-preprocess';
import typescript from '@rollup/plugin-typescript';
import css from 'rollup-plugin-css-only';
import postcss from 'rollup-plugin-postcss';
import replace from '@rollup/plugin-replace';
import {config as configDotenv} from 'dotenv';
import {rmSync} from "fs";

const production = !process.env.ROLLUP_WATCH;

function serve() {
  let server;

  function toExit() {
    if (server) {
      server.kill(0);
    }
  }

  return {
    writeBundle() {
      if (server) {
        return;
      }
      server = require('child_process').spawn('npm',
          ['run', 'start', '--', '--dev'], {
            stdio: ['ignore', 'inherit', 'inherit'],
            shell: true
          });

      process.on('SIGTERM', toExit);
      process.on('exit', toExit);
    }
  };
}

// https://stackoverflow.com/questions/66268219/hide-raw-svelte-files-from-developer-tools-in-production
function removeSourceMaps() {
  return {
    name: 'removeSourceMaps',
    generateBundle() {
      rmSync('public/build/bundle.css.map', {force: true});
    }
  }
}

configDotenv();

export default {
  input: 'src/main.ts',
  output: {
    sourcemap: true,
    format: 'esm',
    dir: 'public/build',
    name: 'app',
  },
  plugins: [
    replace({
      'process.env.isProd': production,
      'process.env.API_URL': JSON.stringify(process.env.API_URL)
    }),
    svelte({
      preprocess: sveltePreprocess({sourceMap: !production}),
      compilerOptions: {
        dev: !production
      }
    }),
    css({output: 'bundle.css'}),
    postcss(), // for full calendar
    resolve({
      browser: true,
      dedupe: ['svelte']
    }),
    commonjs(),
    typescript({
      sourceMap: !production,
      inlineSources: !production
    }),
    !production && serve(),
    !production && livereload('public'),
    production && terser(),
    production && removeSourceMaps()
  ],
  watch: {
    clearScreen: false
  }
};
