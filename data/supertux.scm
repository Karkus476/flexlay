(display "SuperTux Startup Script\n")

(define *game* 'supertux)
(define *tile-size* 32)
(game-set-tilesize 32 16)
(game-load-resources "tuxtiles.xml")
(game-load-resources "tuxsprites.xml")
(game-load-tiles     "tuxtiles.scm")

(set-window-title "Windstille Editor - SuperTux Mode")

(define (supertux:save-map filename)
  ;; FIXME: This is old style singleton code
  (if (access? filename F_OK)
      (rename-file filename (string-append filename "~")))

  (with-output-to-file filename
    (lambda ()
      (display   ";; Generated by Windstille Editor\n")
      (display   "(supertux-level\n")

      (display   "  (version 1)\n")
      (display   "  (name \"Hello World\")\n")
      (format #t "  (width  ~a)~%" (map-get-width))
      (format #t "  (height ~a)~%" (map-get-height))

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
      (write-field "   " (map-get-width) (editor-tilemap-get-data *tilemap*))
      (display     "   )\n\n")
      
      (cond (#f
             (format #t "  (objects\n")
             (for-each (lambda (el)
                         (let* ((obj (editor-objectmap-get-object el)))
                           (format #t "    (~a  (pos ~a ~a))~%" 
                                   (caaddr obj)
                                   (car obj)
                                   (cadr obj)
                                   )))
                       (editor-objectmap-get-objects))
             (format #t "  )\n")))

      (format #t "   )\n\n")

      (newline)
      (display ";; EOF ;;\n")

      (editor-map-set-unmodified (editor-map-component-get-map *editor-map*))
      )))


;; EOF ;;
