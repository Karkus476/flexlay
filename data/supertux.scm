(use-modules (oop goops))
(display "SuperTux Startup Script\n")

(define *game* 'supertux)
(define *tile-size* 32)
(game-set-tilesize 32 16)
(game-load-resources "tuxtiles.xml")
(game-load-resources "tuxsprites.xml")
(game-load-tiles     "tuxtiles.scm")

(set-window-title "Windstille Editor - SuperTux Mode")

;; Metadata for a SuperTux level
(define-class <supertux-level> ()
  (name   #:init-value "Hello World"
          #:accessor supertux:name)
                                        ;  (width  #:init-value 20
                                        ;          #:accessor supertux:width)
                                        ;  (height #:init-value 15
                                        ;          #:accessor supertux:height)
  (background #:init-value "" 
              #:accessor supertux:background)
  (music      #:init-value "Mortimers_chipdisko.mod"
              #:accessor supertux:music)
  (bkgd_red   #:init-value 150
              #:accessor supertux:bkgd_red)
  (bkgd_green #:init-value 200
              #:accessor supertux:bkgd_green)
  (bkgd_blue  #:init-value 255
              #:accessor supertux:bkgd_blue)
  (time       #:init-value 500
              #:accessor supertux:time)
  (gravity    #:init-value 10
              #:accessor supertux:gravity)
  (particle_system #:init-value ""
                   #:accessor supertux:particle-system)
  (theme      #:init-value "antarctica"
              #:accessor supertux:theme)
  (interactive-tm #:init-value #f
                  #:accessor supertux:interactive-tm)
  (foreground-tm  #:init-value #f
                  #:accessor supertux:foreground-tm)
  (background-tm  #:init-value #f 
                  #:accessor supertux:background-tm)
  (objmap #:init-value #f 
          #:accessor supertux:objmap))


(define (supertux:create-levelmap width height)
  (let ((level    (make <supertux-level>))
        (levelmap (editor-map-create)))
    
    (set! (supertux:foreground-tm  level) (editor-tilemap-create width height *tile-size*))
    (set! (supertux:interactive-tm level) (editor-tilemap-create width height *tile-size*))
    (set! (supertux:background-tm  level) (editor-tilemap-create width height *tile-size*))
    (set! (supertux:objmap         level) (editor-objmap-create))
    
    (editor-map-add-layer levelmap (supertux:background-tm  level))
    (editor-map-add-layer levelmap (supertux:interactive-tm level))
    (editor-map-add-layer levelmap (supertux:foreground-tm  level))
    (editor-map-add-layer levelmap (supertux:objmap         level))
    
    ;; FIXME: this doesn't look all that nice here
    (tilemap-paint-tool-set-tilemap (supertux:interactive-tm level))

    (editor-map-set-filename levelmap "/tmp/foobar.stlv")
    (editor-map-set-metadata levelmap level)
    levelmap))

(define (supertux:save-map filename)
  ;; FIXME: This is old style singleton code
  (if (access? filename F_OK)
      (rename-file filename (string-append filename "~")))

  (let* ((levelmap (editor-map-component-get-map *editor-map*))
         (level    (editor-map-get-metadata levelmap)))
    (format #t "Level: ~a~%" level)
    (with-output-to-file filename
      (lambda ()
        (cond ((not level)
               ;; Old style save code
               (display   ";; Generated by Windstille Editor\n")
               (display   "(supertux-level\n")

               (display   "  (version 1)\n")
               (display   "  (name \"Hello World\")\n")
               (format #t "  (width  ~a)~%" (editor-tilemap-get-width  *tilemap))
               (format #t "  (height ~a)~%" (editor-tilemap-get-height *tilemap))

               (format #t "  (background \"arctis.png\")\n")
               (format #t "  (music  \"~a\")~%" "Mortimers_chipdisko.mod")

               (format #t "  (bkgd_red    ~a)~%" 150)
               (format #t "  (bkgd_green  ~a)~%" 200)
               (format #t "  (bkgd_blue   ~a)~%" 255)

               (format #t "  (time  ~a)~%" 500)
               (format #t "  (gravity  ~a)~%" 10)
               (format #t "  (particle_system \"snow\")\n")
               (format #t "  (theme \"antarctica\")\n")

               (display     "  (interactive-tm\n")
               (write-field "   " (editor-tilemap-get-width  *tilemap) (editor-tilemap-get-data *tilemap*))
               (display     "   )\n\n")
               (format #t "   )\n\n")

               (newline)
               (display ";; EOF ;;\n"))
              (else
               ;; New style save code
               (display   ";; Generated by Windstille Editor\n")
               (display   "(supertux-level\n")

               (display   "  (version 1)\n")
               (format #t "  (name ~s)~%"   (supertux:name level))
               (format #t "  (width  ~a)~%" (editor-tilemap-get-width  (supertux:interactive-tm level)))
               (format #t "  (height ~a)~%" (editor-tilemap-get-height (supertux:interactive-tm level)))

               (format #t "  (background ~s)~%" (supertux:background level))
               (format #t "  (music ~s)~%" (supertux:music level))

               (format #t "  (bkgd_red    ~a)~%" (supertux:bkgd_red level))
               (format #t "  (bkgd_green  ~a)~%" (supertux:bkgd_green level))
               (format #t "  (bkgd_blue   ~a)~%" (supertux:bkgd_blue level))

               (format #t "  (time  ~a)~%" (supertux:time level))
               (format #t "  (gravity  ~a)~%" (supertux:gravity level))
               (format #t "  (particle_system ~s)~%" (supertux:particle-system level))
               (format #t "  (theme ~s)~%" (supertux:theme level))

               (let ((width (editor-tilemap-get-width (supertux:interactive-tm level))))
                 (display     "  (interactive-tm\n")
                 (write-field "   " width
                              (editor-tilemap-get-data (supertux:interactive-tm level)))
                 (display     "   )\n\n")

                 (display     "  (background-tm\n")
                 (write-field "   " width
                              (editor-tilemap-get-data (supertux:background-tm level)))
                 (display     "   )\n\n")

                 (display     "  (foreground-tm\n")
                 (write-field "   " width
                              (editor-tilemap-get-data (supertux:foreground-tm level)))
                 (display     "   )\n\n"))
               
               (format #t "  (objects\n")
               (for-each (lambda (el)
                           (let* ((obj (editor-objectmap-get-object (supertux:objmap level) el)))
                             (format #t "    (~a  (x ~a) (y ~a))~%" 
                                     (caaddr obj)
                                     (car obj)
                                     (cadr obj)
                                     )))
                         (editor-objectmap-get-objects (supertux:objmap level)))
               (format #t "  )\n")

               (format #t "   )\n\n")

               (newline)
               (display ";; EOF ;;\n")))))
    (editor-map-set-unmodified levelmap)))

(define (supertux:load-map filename)
  (catch #t
         (lambda ()
           (let ((levelmap (supertux:create-level-map-from-file filename)))
             (editor-map-component-set-map *editor-map* levelmap)
             (add-buffer levelmap)
             ))
         (lambda args
           (editor-error args)))
  (push-last-file filename))

(define (supertux:create-level-map-from-file filename)
  (display "Loading SuperTux level: ")
  (display filename)
  (newline)
  (let ((data (with-input-from-file filename
                (lambda () (cdr (read)))))
        (level (make <supertux-level>)))
    ;; read in the level metadata
    (set! (supertux:name  level)       (get-value-from-tree '(name _) data 20))
    (set! (supertux:theme level)      (get-value-from-tree '(theme _) data "antarctica"))
    (set! (supertux:music level)      (get-value-from-tree '(music _) data "Mortimers_chipdisko.mod"))
    (set! (supertux:background level) (get-value-from-tree '(background _)   data "arctis.png"))
    (set! (supertux:bkgd_red   level) (get-value-from-tree '(bkgd_red _)     data 150))
    (set! (supertux:bkgd_green level) (get-value-from-tree '(bkgd_green _)   data 200))
    (set! (supertux:bkgd_blue  level) (get-value-from-tree '(bkgd_blue _)    data 255))
    (set! (supertux:time  level)      (get-value-from-tree '(time _)         data 250))
    (set! (supertux:particle-system level)     (get-value-from-tree '(particle_system _) data ""))
    (set! (supertux:gravity         level)     (get-value-from-tree '(gravity _)      data 10))

    (let ((width   (get-value-from-tree '(width _)    data 20))
          (height  (get-value-from-tree '(height _)   data 15))
          (objects (get-value-from-tree '(objects)   data '()))
          (interactive-tm (get-value-from-tree '(interactive-tm) data '()))
          (background-tm  (get-value-from-tree '(background-tm)  data '()))
          (foreground-tm  (get-value-from-tree '(foreground-tm)  data '())))

      ;; load level file and extract tiledata and w/h
      (let* ((m       (editor-map-create))
             (objmap  (editor-objmap-create)))

        (set! (supertux:objmap          level) objmap)
        (set! (supertux:interactive-tm  level) (editor-tilemap-create width height *tile-size*))
        (set! (supertux:background-tm   level) (editor-tilemap-create width height *tile-size*))
        (set! (supertux:foreground-tm   level) (editor-tilemap-create width height *tile-size*))
        (set! *tilemap* (supertux:interactive-tm  level))

        ;; set data to the tilemap
        (if (not (null? interactive-tm))
            (editor-tilemap-set-data (supertux:interactive-tm level) interactive-tm)
            (display "Error: interactive-tm missing\n"))
        (if (not (null? foreground-tm))
            (editor-tilemap-set-data (supertux:foreground-tm level) foreground-tm)
            (display "Error: foreground-tm missing\n"))
        (if (not (null? background-tm))
            (editor-tilemap-set-data (supertux:background-tm level) background-tm)
            (display "Error: background-tm missing\n"))

        (display (supertux:interactive-tm level))(newline)

        (for-each (lambda (el)
                    (let ((x (get-value-from-tree '(x _) (cdr el) 0))
                          (y (get-value-from-tree '(y _) (cdr el) 0)))
                      (case (car el)
                        ((mriceblock)
                         (objectmap-add-object objmap "sprites/mriceblock" x y '(mriceblock)))
                        ((mrbomb)
                         (objectmap-add-object objmap "sprites/mrbomb" x y '(mrbomb)))
                        ((spawnpoint)
                         (objectmap-add-object objmap "sprites/spawnpoint" x y '(outpost)))
                        ((outpost)
                         (objectmap-add-object objmap "sprites/outpost"  x y '(spawnpoint)))
                        )))
                  objects)
        
        (editor-map-add-layer m (supertux:background-tm  level))
        (editor-map-add-layer m (supertux:interactive-tm level))
        (editor-map-add-layer m (supertux:foreground-tm  level))

        (editor-tilemap-set-bgcolor (supertux:background-tm  level) 150 200 255 255)

        (editor-map-add-layer m (supertux:objmap         level))

        ;; FIXME: this doesn't look all that nice here
        (tilemap-paint-tool-set-tilemap (supertux:interactive-tm level))

        (editor-map-set-filename m filename)
        (editor-map-set-metadata m level)
        m))))

(define (supertux:set-active-layer layer)
  (let ((level (editor-map-get-metadata (editor-map-component-get-map *editor-map*))))
    (case layer
      ((background)
       (editor-tilemap-set-fgcolor (supertux:background-tm  level) 255 255 255 255)
       (editor-tilemap-set-fgcolor (supertux:interactive-tm level) 255 150 150 150)
       (editor-tilemap-set-fgcolor (supertux:foreground-tm  level) 255 150 150 150)
       (tilemap-paint-tool-set-tilemap (supertux:background-tm level)))

      ((interactive)
       (editor-tilemap-set-fgcolor (supertux:background-tm  level) 255 150 150 150)
       (editor-tilemap-set-fgcolor (supertux:interactive-tm level) 255 255 255 255)
       (editor-tilemap-set-fgcolor (supertux:foreground-tm  level) 255 150 150 150)
       (tilemap-paint-tool-set-tilemap (supertux:interactive-tm level)))

      ((foreground)
       (editor-tilemap-set-fgcolor (supertux:background-tm  level) 255 150 150 150)
       (editor-tilemap-set-fgcolor (supertux:interactive-tm level) 255 150 150 150)
       (editor-tilemap-set-fgcolor (supertux:foreground-tm  level) 255 255 255 255)
       (tilemap-paint-tool-set-tilemap (supertux:foreground-tm level))))))

;; EOF ;;
