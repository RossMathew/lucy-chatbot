module.exports = function(grunt) {

  grunt.initConfig({
    jshint: {
      files: ['Gruntfile.js', 'static/js/**/*.js'],
      options: {
        globals: {
          jQuery: true
        }
      }
    },

    sass: {
      dist: {
        options: {
          style: 'expanded',
          sourcemap: 'none'
        },
        files: {
          'static/styles/main.css': ['static/styles/rsquare.scss']
        }
      }
    },
    watch: {

      autolivereload:{
        options: {
          livereload: 1337
        },
         files: ['static/js/**/*.js', 'static/styles/**/*.css', 'website/**/*.html', 'projects/**/*.html', '**/*.py'],

      },
      concatcss: {
      options: {
        livereload: true
      },
          files: ['static/styles/rsquare.scss', 'static/styles/**/*.scss'],
          tasks: ['sass']
      },

      concatjs: {
      options: {
        livereload: true
      },

             files: ['static/js/*.js', 'static/js/**/*.js'],
             tasks: ['jshint']

        }


    },
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-sass');

  grunt.registerTask('jshint', ['jshint']);
  grunt.registerTask('default', ['sass', 'watch:concatcss']);
  grunt.registerTask('livereload',['watch:autolivereload'])
};
