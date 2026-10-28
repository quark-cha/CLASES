<?php

// BEGIN PROJECT_SUBDIRECTORIES: bloque autonomo para plantillas web-base.
function project_directory_escape($value) {
    return htmlspecialchars((string)$value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}
function project_directory_language() {
    $language = $_GET['idioma'] ?? substr($_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? 'es', 0, 2);
    return is_string($language) && preg_match('/^[a-z]{2}$/i', $language) ? strtolower($language) : 'es';
}
function project_directory_label($key, $language) {
    $labels = [
        'directories' => ['es'=>'Subdirectorios', 'en'=>'Subdirectories', 'fr'=>'Sous-répertoires', 'it'=>'Sottocartelle'],
        'back' => ['es'=>'Volver al catálogo', 'en'=>'Back to catalog', 'fr'=>'Retour au catalogue', 'it'=>'Torna al catalogo'],
        'files' => ['es'=>'Archivos', 'en'=>'Files', 'fr'=>'Fichiers', 'it'=>'File'],
        'empty' => ['es'=>'No hay archivos en este directorio.', 'en'=>'There are no files in this directory.', 'fr'=>'Aucun fichier dans ce répertoire.', 'it'=>'Questa cartella non contiene file.'],
    ];
    return $labels[$key][$language] ?? $labels[$key]['en'];
}
function project_directory_path($base, $relative) {
    if (!is_string($relative) || $relative === '' || preg_match('/[\\\\\x00-\x1f]/', $relative)) return null;
    foreach (explode('/', $relative) as $part) {
        if ($part === '' || $part[0] === '.' || in_array($part, ['web-base', '__pycache__'], true)) return null;
    }
    $root = realpath($base);
    $candidate = realpath($base . DIRECTORY_SEPARATOR . $relative);
    if (!$root || !$candidate || !is_dir($candidate) || is_link($base . DIRECTORY_SEPARATOR . $relative)) return null;
    return strpos($candidate, rtrim($root, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR) === 0 ? $candidate : null;
}
function project_directory_names($base, $relative = '') {
    $path = $relative === '' ? $base : project_directory_path($base, $relative);
    if (!$path) return [];
    $entries = @scandir($path);
    if ($entries === false) return [];
    $names = [];
    foreach ($entries as $name) {
        if ($name === '' || $name[0] === '.' || in_array($name, ['web-base', '__pycache__'], true)) continue;
        $child = $relative === '' ? $name : $relative . '/' . $name;
        if (project_directory_path($base, $child)) $names[] = $name;
    }
    usort($names, 'strnatcasecmp');
    return $names;
}
function project_directory_url($base, $relative, $language) {
    $path = project_directory_path($base, $relative);
    $encoded = implode('/', array_map('rawurlencode', explode('/', $relative)));
    if ($path && (is_file($path . '/index.php') || is_file($path . '/index.html'))) {
        return $encoded . '/?idioma=' . rawurlencode($language);
    }
    return '?carpeta=' . rawurlencode($relative) . '&idioma=' . rawurlencode($language);
}
function project_subdirectories_nav($base, $language, $relative = '') {
    $names = project_directory_names($base, $relative);
    if (!$names) return;
    echo '<nav class="project-subdirectories" aria-label="' . project_directory_escape(project_directory_label('directories', $language)) . '" style="margin:16px 0 22px;padding:14px;border:1px solid #d9e1e8;border-radius:8px;background:#f7f9fb">';
    echo '<strong style="display:block;margin-bottom:10px">' . project_directory_escape(project_directory_label('directories', $language)) . '</strong><div style="display:flex;gap:8px;flex-wrap:wrap">';
    foreach ($names as $name) {
        $child = $relative === '' ? $name : $relative . '/' . $name;
        echo '<a style="display:inline-flex;align-items:center;padding:8px 12px;border:1px solid #b9d0db;border-radius:6px;color:#0f6674;background:#fff;text-decoration:none" href="' . project_directory_escape(project_directory_url($base, $child, $language)) . '">&#128193; ' . project_directory_escape($name) . '/</a>';
    }
    echo '</div></nav>';
}
function project_directory_browser($base) {
    $relative = $_GET['carpeta'];
    $path = project_directory_path($base, $relative);
    $entries = $path ? @scandir($path) : false;
    if ($entries === false) {
        http_response_code(404);
        exit('Directorio no disponible');
    }
    $language = project_directory_language();
    $title = basename($base) . ' / ' . $relative . '/';
    echo '<!doctype html><html lang="' . project_directory_escape($language) . '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' . project_directory_escape($title) . '</title></head><body style="font-family:Arial,sans-serif;color:#17202a;margin:0"><main style="max-width:1100px;margin:auto;padding:28px 16px">';
    echo '<a href="?idioma=' . project_directory_escape($language) . '">' . project_directory_escape(project_directory_label('back', $language)) . '</a><h1>' . project_directory_escape($title) . '</h1>';
    project_subdirectories_nav($base, $language, $relative);
    echo '<h2>' . project_directory_escape(project_directory_label('files', $language)) . '</h2><ul style="padding-left:24px;line-height:2">';
    $count = 0;
    foreach ($entries as $name) {
        if ($name === '' || $name[0] === '.' || !is_file($path . '/' . $name) || is_link($path . '/' . $name)) continue;
        $href = implode('/', array_map('rawurlencode', explode('/', $relative . '/' . $name)));
        echo '<li><a href="' . project_directory_escape($href) . '">' . project_directory_escape($name) . '</a> <small>(' . (int)filesize($path . '/' . $name) . ' bytes)</small></li>';
        $count++;
    }
    echo '</ul>';
    if (!$count) echo '<p>' . project_directory_escape(project_directory_label('empty', $language)) . '</p>';
    echo '</main></body></html>';
    exit;
}
if (isset($_GET['carpeta'])) project_directory_browser(__DIR__);
// END PROJECT_SUBDIRECTORIES

// index.php - catalogo local reutilizable para directorios de proyecto.
// Escanea los archivos reales del directorio y usa catalogo.cat solo como
// diccionario de titulos traducidos. Si falta catalogo.cat, funciona con
// nombres limpios derivados de los archivos.

$idiomas_soportados = ['es', 'en', 'fr', 'it', 'pt', 'de', 'ar', 'jp', 'ru', 'ch'];
$idioma_get = isset($_GET['idioma']) ? strtolower(trim($_GET['idioma'])) : '';
$idioma_nav = strtolower(substr($_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? 'es', 0, 2));
$idioma = $idioma_get !== '' ? $idioma_get : $idioma_nav;

if (strpos($idioma, 'es') === 0) {
    $idioma = 'es';
}
if (!in_array($idioma, $idiomas_soportados, true)) {
    $idioma = 'en';
}

$mostrar_otros = isset($_GET['otros']) && $_GET['otros'] === '1';

$dir = __DIR__;
$project_name = basename($dir);

function h($value) {
    return htmlspecialchars((string)$value, ENT_QUOTES, 'UTF-8');
}

function clean_title_from_slug($slug) {
    $slug = preg_replace('/[_-]+/', ' ', $slug);
    $slug = trim($slug);
    return mb_convert_case($slug, MB_CASE_TITLE, 'UTF-8');
}

function clean_title_from_filename($filename) {
    $stem = pathinfo($filename, PATHINFO_FILENAME);
    $stem = preg_replace('/^[A-Za-z]{2}_/', '', $stem);
    $stem = preg_replace('/^\d+[_\-\s]*/', '', $stem);
    if ($stem === '') {
        $stem = pathinfo($filename, PATHINFO_FILENAME);
    }
    return clean_title_from_slug($stem);
}

function clean_title_from_unprefixed_filename($filename) {
    $stem = pathinfo($filename, PATHINFO_FILENAME);
    return clean_title_from_slug($stem);
}

function normalize_lang($lang) {
    $lang = strtolower(trim((string)$lang));
    if (strpos($lang, 'es') === 0) return 'es';
    return substr($lang, 0, 2);
}

function normalize_doc_id($id) {
    $id = trim((string)$id);
    if ($id !== '' && ctype_digit($id)) {
        return (string)intval($id);
    }
    return $id;
}

function doc_id_variants($id) {
    $id = trim((string)$id);
    if ($id === '') {
        return [];
    }

    $variants = [$id];
    if (ctype_digit($id)) {
        $plain = (string)intval($id);
        $variants[] = $plain;
        $variants[] = str_pad($plain, 2, '0', STR_PAD_LEFT);
        $variants[] = str_pad($plain, 3, '0', STR_PAD_LEFT);
    }

    return array_values(array_unique($variants));
}

function read_catalog_cat($path) {
    if (!is_file($path)) {
        return ['headers' => [], 'rows' => []];
    }

    $fh = fopen($path, 'r');
    if (!$fh) {
        return ['headers' => [], 'rows' => []];
    }

    $headers = [];
    $rows = [];
    $line_no = 0;

    while (($data = fgetcsv($fh, 0, ';')) !== false) {
        $line_no++;
        if ($line_no === 1) {
            $headers = array_map(function ($item) {
                $item = preg_replace('/^\xEF\xBB\xBF/u', '', (string)$item);
                return strtolower(trim($item));
            }, $data);
            continue;
        }

        if (!$headers || count($data) === 0) continue;
        $row = [];
        foreach ($headers as $i => $key) {
            $row[$key] = isset($data[$i]) ? trim((string)$data[$i]) : '';
        }
        $id = $row['id'] ?? '';
        if ($id !== '') {
            foreach (doc_id_variants($id) as $variant) {
                $rows[$variant] = $row;
            }
        }
    }

    fclose($fh);
    return ['headers' => $headers, 'rows' => $rows];
}

function read_menu_csv($path) {
    $fallback = [
        'title' => ['es' => 'Catalogo del proyecto', 'en' => 'Project catalog'],
        'open' => ['es' => 'Abrir documento', 'en' => 'Open document'],
        'request' => ['es' => 'Pedir traduccion', 'en' => 'Request translation'],
        'home' => ['es' => 'Inicio', 'en' => 'Home'],
        'projects' => ['es' => 'Proyectos', 'en' => 'Projects'],
        'catalog' => ['es' => 'Catalogo general', 'en' => 'Main catalog'],
        'top' => ['es' => 'Arriba', 'en' => 'Top'],
        'numbered' => ['es' => 'Documentos', 'en' => 'Documents'],
        'others' => ['es' => 'Otros', 'en' => 'Other files'],
    ];

    if (!is_file($path)) {
        return $fallback;
    }

    $fh = fopen($path, 'r');
    if (!$fh) {
        return $fallback;
    }

    $headers = [];
    $rows = $fallback;
    $line_no = 0;

    while (($data = fgetcsv($fh, 0, ';')) !== false) {
        $line_no++;
        if ($line_no === 1) {
            $headers = array_map(function ($item) {
                return strtolower(trim((string)$item));
            }, $data);
            continue;
        }

        if (!$headers || count($data) === 0) continue;
        $key = trim((string)($data[0] ?? ''));
        if ($key === '') continue;
        if (!isset($rows[$key])) $rows[$key] = [];

        foreach ($headers as $i => $lang) {
            if ($i === 0 || $lang === '' || $lang === 'key') continue;
            $value = trim((string)($data[$i] ?? ''));
            if ($value !== '') {
                $rows[$key][$lang] = $value;
            }
        }
    }

    fclose($fh);
    return $rows;
}

function menu_text($menu, $key, $lang) {
    if (isset($menu[$key][$lang]) && $menu[$key][$lang] !== '') {
        return $menu[$key][$lang];
    }
    if (isset($menu[$key]['en']) && $menu[$key]['en'] !== '') {
        return $menu[$key]['en'];
    }
    if (isset($menu[$key]['es']) && $menu[$key]['es'] !== '') {
        return $menu[$key]['es'];
    }
    return $key;
}

function parse_project_file($filename) {
    if (preg_match('/^([A-Za-z]{2})_(\d+)(?:_|-|\s)?(.*?)\.(pdf|html|htm|mp3|wav)$/i', $filename, $m)) {
        return [
            'lang' => normalize_lang($m[1]),
            'id' => normalize_doc_id($m[2]),
            'slug' => trim($m[3], "_- \t\n\r\0\x0B"),
            'ext' => strtolower($m[4]),
            'file' => $filename,
            'prefixed' => true,
        ];
    }

    if (preg_match('/^(\d+)(?:_|-|\s)?(.*?)\.(pdf|html|htm|mp3|wav)$/i', $filename, $m)) {
        return [
            'lang' => 'generic',
            'id' => normalize_doc_id($m[1]),
            'slug' => trim($m[2], "_- \t\n\r\0\x0B"),
            'ext' => strtolower($m[3]),
            'file' => $filename,
            'prefixed' => false,
        ];
    }

    return null;
}

function parse_other_pdf_file($filename) {
    if (!preg_match('/\.pdf$/i', $filename)) {
        return null;
    }
    if (parse_project_file($filename) !== null) {
        return null;
    }

    $stem = pathinfo($filename, PATHINFO_FILENAME);
    $lang = 'generic';
    $slug = $stem;
    $prefixed = false;

    if (preg_match('/^([A-Za-z]{2})_(.+)$/', $stem, $m)) {
        $candidate = normalize_lang($m[1]);
        if (in_array($candidate, $GLOBALS['idiomas_soportados'], true)) {
            $lang = $candidate;
            $slug = $m[2];
            $prefixed = true;
        }
    }

    $key = mb_strtolower($slug, 'UTF-8');
    $key = preg_replace('/[_\-\s]+/', ' ', $key);
    $key = trim($key);
    if ($key === '') {
        $key = mb_strtolower($stem, 'UTF-8');
    }

    return [
        'key' => $key,
        'lang' => $lang,
        'slug' => $slug,
        'file' => $filename,
        'prefixed' => $prefixed,
    ];
}

function best_lang_for_doc($doc, $preferred) {
    if (isset($doc['files'][$preferred]['pdf'])) return $preferred;
    if (isset($doc['files']['en']['pdf'])) return 'en';
    if (isset($doc['files']['es']['pdf'])) return 'es';
    return null;
}

function doc_has_lang($doc, $lang) {
    return isset($doc['files'][$lang]['pdf']);
}

function best_lang_for_other($item, $preferred) {
    if (isset($item['files'][$preferred])) return $preferred;
    if (isset($item['files']['en'])) return 'en';
    if (isset($item['files']['es'])) return 'es';
    if (isset($item['files']['generic'])) return 'generic';
    foreach ($item['files'] as $lang => $file) {
        return $lang;
    }
    return null;
}

function other_has_lang($item, $lang) {
    return isset($item['files'][$lang]);
}

function display_lang_code($lang) {
    return $lang === 'generic' ? 'ES' : strtoupper((string)$lang);
}

function title_for_doc($doc, $cat_rows, $preferred) {
    $id = $doc['id'];
    $row = [];
    foreach (doc_id_variants($id) as $variant) {
        if (isset($cat_rows[$variant])) {
            $row = $cat_rows[$variant];
            break;
        }
    }
    $candidates = [$preferred, 'en', 'es'];

    foreach ($candidates as $lang) {
        $lang = strtolower((string)$lang);
        $value = $row[$lang] ?? $row[strtoupper($lang)] ?? '';
        if ($value !== '') return $value;
    }

    if (isset($doc['files']['es']['pdf'])) {
        return clean_title_from_filename($doc['files']['es']['pdf']);
    }

    if (isset($doc['base_file'])) {
        return clean_title_from_filename($doc['base_file']);
    }

    if (isset($doc['generic_file'])) {
        return clean_title_from_unprefixed_filename($doc['generic_file']);
    }

    return clean_title_from_slug('Documento ' . $id);
}

function title_for_other($item, $preferred) {
    $lang = best_lang_for_other($item, $preferred);
    if ($lang !== null && isset($item['files'][$lang])) {
        return clean_title_from_filename($item['files'][$lang]);
    }
    if (isset($item['base_file'])) {
        return clean_title_from_filename($item['base_file']);
    }
    return clean_title_from_slug($item['slug'] ?? $item['key'] ?? 'Documento');
}

$cat = read_catalog_cat($dir . DIRECTORY_SEPARATOR . 'catalogo.cat');
$menu = read_menu_csv($dir . DIRECTORY_SEPARATOR . 'index.csv');
$docs = [];
$otros = [];

foreach (scandir($dir) as $file) {
    if ($file === '.' || $file === '..') continue;
    $parsed = parse_project_file($file);
    if (!$parsed) {
        $other = parse_other_pdf_file($file);
        if (!$other) continue;

        $key = $other['key'];
        if (!isset($otros[$key])) {
            $otros[$key] = [
                'key' => $key,
                'slug' => $other['slug'],
                'files' => [],
            ];
        }

        $otros[$key]['files'][$other['lang']] = $other['file'];
        if ($other['prefixed'] && !isset($otros[$key]['base_file'])) {
            $otros[$key]['base_file'] = $other['file'];
        }
        if (!$other['prefixed'] && !isset($otros[$key]['generic_file'])) {
            $otros[$key]['generic_file'] = $other['file'];
        }
        continue;
    }

    $id = $parsed['id'];
    if (!isset($docs[$id])) {
        $docs[$id] = [
            'id' => $id,
            'slug' => $parsed['slug'],
            'files' => [],
        ];
    }

    if ($docs[$id]['slug'] === '' && $parsed['slug'] !== '') {
        $docs[$id]['slug'] = $parsed['slug'];
    }

    $docs[$id]['files'][$parsed['lang']][$parsed['ext']] = $parsed['file'];

    if ($parsed['prefixed'] && !isset($docs[$id]['base_file'])) {
        $docs[$id]['base_file'] = $parsed['file'];
    }
    if (!$parsed['prefixed'] && !isset($docs[$id]['generic_file'])) {
        $docs[$id]['generic_file'] = $parsed['file'];
    }
}

uksort($docs, function ($a, $b) {
    if (is_numeric($a) && is_numeric($b)) return intval($a) <=> intval($b);
    if (is_numeric($a)) return -1;
    if (is_numeric($b)) return 1;
    return strnatcasecmp((string)$a, (string)$b);
});

uasort($otros, function ($a, $b) use ($idioma) {
    $lang_a = best_lang_for_other($a, $idioma);
    $lang_b = best_lang_for_other($b, $idioma);
    $rank = function ($lang) use ($idioma) {
        if ($lang === $idioma) return 0;
        if ($lang === 'en') return 1;
        if ($lang === 'es') return 2;
        if ($lang === 'generic') return 3;
        return 4;
    };
    $ra = $rank($lang_a);
    $rb = $rank($lang_b);
    if ($ra !== $rb) return $ra <=> $rb;
    return strnatcasecmp(title_for_other($a, $idioma), title_for_other($b, $idioma));
});

$title_text = menu_text($menu, 'title', $idioma);

function current_project_url_path() {
    $script = $_SERVER['SCRIPT_NAME'] ?? '';
    $dir = rtrim(str_replace('\\', '/', dirname($script)), '/');
    return $dir === '' ? '/' : $dir . '/';
}

function project_file_path_for_get($pdf_file) {
    return current_project_url_path() . $pdf_file;
}

function md_exists_for_pdf($dir, $pdf_file) {
    $stem = pathinfo($pdf_file, PATHINFO_FILENAME);
    return is_file($dir . DIRECTORY_SEPARATOR . 'md' . DIRECTORY_SEPARATOR . $stem . '.md');
}

function open_url_for_pdf($dir, $pdf_file) {
    return rawurlencode($pdf_file);
}

function reader_url_for_pdf($pdf_file) {
    return '?doc=' . rawurlencode($pdf_file) . '&idioma=' . rawurlencode($GLOBALS['idioma']);
}

function translation_request_url($lang, $pdf_file) {
    $pdf_path = project_file_path_for_get($pdf_file);
    return '/peticion_traduccion.php?idioma=' . rawurlencode($lang) .
        '&trabajo=' . rawurlencode($pdf_path);
}

function language_button_content($lang) {
    $flag = language_flag_name($lang);
    if ($flag !== '') {
        return '<img class="flag only" src="/teorias/' . h(rawurlencode($flag)) . '" alt="' . h(language_label($lang)) . '" title="' . h(language_label($lang)) . '">';
    }

    return h(strtoupper($lang));
}

function language_has_flag($lang) {
    return language_flag_name($lang) !== '';
}

function language_flag_name($lang) {
    $code = strtoupper($lang);
    $lower = strtolower($lang);
    $candidates = [
        $code . '.png',
        $lower . '.png',
        $code . '.jpeg',
        $lower . '.jpeg',
        $code . '.jpg',
        $lower . '.jpg',
    ];

    foreach ($candidates as $name) {
        $flag_fs = dirname(dirname(__DIR__)) . DIRECTORY_SEPARATOR . $name;
        if (is_file($flag_fs)) {
            return $name;
        }
    }

    return '';
}

function language_label($lang) {
    $labels = [
        'es' => 'Espanol',
        'en' => 'English',
        'fr' => 'Francais',
        'it' => 'Italiano',
        'pt' => 'Portugues',
        'de' => 'Deutsch',
        'ar' => 'Arabic',
        'jp' => 'Japanese',
        'ru' => 'Russian',
        'ch' => 'Chinese',
    ];
    $key = strtolower((string)$lang);
    return $labels[$key] ?? strtoupper($key);
}

function audio_button_content() {
    $candidates = ['AUDIO.png', 'audio.png', 'ALTAVOZ.png', 'altavoz.png', 'SPEAKER.png', 'speaker.png', 'SONIDO.png', 'sonido.png'];
    foreach ($candidates as $name) {
        $fs = dirname(dirname(__DIR__)) . DIRECTORY_SEPARATOR . $name;
        if (is_file($fs)) {
            return '<img class="audio-icon" src="/teorias/' . h(rawurlencode($name)) . '" alt="Audio" title="Audio">';
        }
    }
    return '&#128266;';
}

function filtra_MD(string $md): string {
    $text = str_replace(["\r\n", "\r"], "\n", $md);
    $text = preg_replace('/```.*?```/s', '', $text);
    $text = preg_replace('/^(?: {4}|\t).*$/m', '', $text);
    $text = preg_replace('/!\[([^\]]*)\]\([^)]+\)/', '$1', $text);
    $text = preg_replace('/\[([^\]]+)\]\([^)]+\)/', '$1', $text);
    $text = preg_replace('/^\s*\[[^\]]+\]:\s*\S+.*$/m', '', $text);
    $text = preg_replace(['/(\*\*\*|___)(.*?)(\*\*\*|___)/s', '/(\*\*|__)(.*?)(\*\*|__)/s', '/(\*|_)(.*?)(\*|_)/s'], '$2', $text);
    $text = preg_replace('/^\s*[-\*\+]\s+/m', '', $text);
    $text = preg_replace('/^\s*\d+\.\s+/m', '', $text);
    $text = preg_replace('/^\s*>\s?/m', '', $text);
    $text = preg_replace('/`([^`]+)`/', '$1', $text);
    $text = strip_tags($text);
    $text = html_entity_decode($text, ENT_QUOTES | ENT_HTML5, 'UTF-8');
    $text = preg_replace('/\[(.*?)\]\[\d+\]/', '$1', $text);
    $text = str_replace(['\\', '*', '_', '`', '~'], '', $text);
    $text = str_replace('#', '. ', $text);
    $text = preg_replace("/[ \t]{2,}/", " ", $text);
    $text = preg_replace("/\n{3,}/", "\n\n", $text);
    return trim($text);
}

function obtenerIdiomaSintesis($codigo_iso) {
    $mapa_idiomas = [
        'es' => 'es-ES', 'en' => 'en-US', 'fr' => 'fr-FR', 'it' => 'it-IT',
        'de' => 'de-DE', 'pt' => 'pt-PT', 'ru' => 'ru-RU', 'jp' => 'ja-JP',
        'ja' => 'ja-JP', 'ch' => 'zh-CN', 'zh' => 'zh-CN', 'ar' => 'ar-SA',
    ];
    return $mapa_idiomas[strtolower((string)$codigo_iso)] ?? 'es-ES';
}

function extract_abstract_section($content, $doc_id) {
    $variants = array_map(function ($variant) {
        return preg_quote((string)$variant, '/');
    }, doc_id_variants($doc_id));
    if (!$variants) {
        return '';
    }

    $pattern = '/^#\s+[A-Za-z]{2}_(?:' . implode('|', $variants) . ')\s*:[^\n]*\n+(?:^##\s+[^\n]*\n+)?(.*?)(?=^---\s*$|^#\s+[A-Za-z]{2}_\d+\s*:|\z)/msu';
    if (preg_match($pattern, $content, $m)) {
        return trim($m[1]);
    }
    return '';
}

function abstract_for_pdf($dir, $project_name, $pdf_file, $parsed_doc, $chosen_lang) {
    $stem = pathinfo($pdf_file, PATHINFO_FILENAME);
    $doc_id = $parsed_doc['id'] ?? '';
    $langs = array_unique([
        strtoupper((string)($parsed_doc['lang'] ?? '')),
        strtoupper((string)$chosen_lang),
        'EN',
        'ES',
    ]);

    $direct_candidates = [
        $dir . DIRECTORY_SEPARATOR . $stem . '.abstract',
        $dir . DIRECTORY_SEPARATOR . 'md' . DIRECTORY_SEPARATOR . $stem . '.abstract',
    ];

    foreach ($direct_candidates as $candidate) {
        if (is_file($candidate)) {
            $text = trim(file_get_contents($candidate));
            if ($text !== '') return $text;
        }
    }

    if ($doc_id === '' || !is_numeric($doc_id)) {
        return '';
    }

    foreach ($langs as $lang) {
        if ($lang === '') continue;
        $candidate = $dir . DIRECTORY_SEPARATOR . $lang . '_TOT_' . $project_name . '.abstract';
        if (!is_file($candidate)) continue;

        $section = extract_abstract_section(file_get_contents($candidate), $doc_id);
        if ($section !== '') return $section;
    }

    return '';
}

function image_for_doc($dir, $parsed_doc, $chosen_lang) {
    $doc_id = $parsed_doc['id'] ?? '';
    if ($doc_id === '' || !is_numeric($doc_id)) {
        return '';
    }

    $langs = array_unique([
        strtoupper((string)($parsed_doc['lang'] ?? '')),
        strtoupper((string)$chosen_lang),
        'EN',
        'ES',
    ]);

    foreach ($langs as $lang) {
        if ($lang === '') continue;
        foreach (doc_id_variants($doc_id) as $variant) {
            $name = $lang . '_' . $variant . '.png';
            if (is_file($dir . DIRECTORY_SEPARATOR . 'png' . DIRECTORY_SEPARATOR . $name)) {
                return 'png/' . $name;
            }
            if (is_file($dir . DIRECTORY_SEPARATOR . $name)) {
                return $name;
            }
        }
    }

    return '';
}

function pdf_is_catalogued($docs, $otros, $pdf_file) {
    $parsed = parse_project_file($pdf_file);
    if ($parsed && $parsed['ext'] === 'pdf') {
        $id = $parsed['id'];
        $lang = $parsed['lang'];
        return isset($docs[$id]['files'][$lang]['pdf']) &&
            $docs[$id]['files'][$lang]['pdf'] === $pdf_file;
    }

    $other = parse_other_pdf_file($pdf_file);
    if (!$other) return false;
    $key = $other['key'];
    $lang = $other['lang'];
    return isset($otros[$key]['files'][$lang]) &&
        $otros[$key]['files'][$lang] === $pdf_file;
}

if (isset($_GET['doc'])) {
    $doc_param = rawurldecode((string)$_GET['doc']);
    $pdf_file = basename($doc_param);

    if ($pdf_file !== $doc_param && $doc_param !== rawurlencode($pdf_file)) {
        http_response_code(400);
        exit("Documento no valido");
    }
    if (!preg_match('/\.pdf$/i', $pdf_file)) {
        http_response_code(400);
        exit("Archivo no valido");
    }
    if (!pdf_is_catalogued($docs, $otros, $pdf_file)) {
        http_response_code(404);
        exit("Documento no incluido en el catalogo");
    }

    $ruta_pdf = $dir . DIRECTORY_SEPARATOR . $pdf_file;
    if (!is_file($ruta_pdf)) {
        http_response_code(404);
        exit("PDF no encontrado");
    }

    if (isset($_GET['directo']) && $_GET['directo'] === '1') {
        header('Content-Type: application/pdf');
        header('Content-Length: ' . filesize($ruta_pdf));
        readfile($ruta_pdf);
        exit;
    }

    $parsed_doc = parse_project_file($pdf_file);
    $parsed_other = $parsed_doc ? null : parse_other_pdf_file($pdf_file);
    $nombre_base = pathinfo($pdf_file, PATHINFO_FILENAME);
    $nombre_md = $nombre_base . '.md';
    $ruta_md = $dir . DIRECTORY_SEPARATOR . 'md' . DIRECTORY_SEPARATOR . $nombre_md;
    $no_md = isset($_GET['no_md']) && $_GET['no_md'] === '1';
    $texto_md = null;
    $idioma_js = obtenerIdiomaSintesis(($parsed_doc['lang'] ?? $parsed_other['lang'] ?? $idioma));

    if (!$no_md && is_file($ruta_md)) {
        $texto_md = filtra_MD(file_get_contents($ruta_md));
    }

    if ($parsed_doc) {
        $titulo_doc = title_for_doc($docs[$parsed_doc['id']], $cat['rows'], $idioma);
        $abstract_doc = abstract_for_pdf($dir, $project_name, $pdf_file, $parsed_doc, $idioma);
        $image_doc = image_for_doc($dir, $parsed_doc, $idioma);
    } else {
        $titulo_doc = title_for_other($otros[$parsed_other['key']] ?? ['files' => [$parsed_other['lang'] => $pdf_file]], $idioma);
        $abstract_doc = abstract_for_pdf($dir, $project_name, $pdf_file, ['id' => '', 'lang' => $parsed_other['lang'] ?? $idioma], $idioma);
        $image_doc = '';
    }
    $pdf_directo = '?doc=' . rawurlencode($pdf_file) . '&directo=1';
?>
<!doctype html>
<html lang="<?php echo h($idioma); ?>">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?php echo h($titulo_doc); ?></title>
<link rel="stylesheet" href="/css/ver_trabajo.css">
<?php if ($texto_md): ?>
<script src="/css/ver_trabajo.js"></script>
<?php endif; ?>
<style>
body{margin:0;font-family:Arial,Helvetica,sans-serif;color:#17202a;background:#fff}
.viewer-head{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:12px 16px;border-bottom:1px solid #d9e1e8;background:#f7f9fb}
.viewer-head a,.viewer-head button{min-height:34px;border:1px solid #d9e1e8;border-radius:6px;background:#fff;color:#0f6674;text-decoration:none;font-weight:700;padding:7px 10px;cursor:pointer}
.voice-controls{display:flex;gap:8px;flex-wrap:wrap}
.viewer-title{font-weight:700}
.doc-image{max-width:980px;margin:14px auto 0}
.doc-image img{width:100%;max-height:360px;object-fit:cover;border-radius:8px;border:1px solid #d9e1e8;display:block}
.abstract-box{max-width:980px;margin:14px auto;padding:14px 16px;border-left:4px solid #0f6674;background:#f7f9fb;line-height:1.55}
.abstract-box h2{font-size:18px;margin:0 0 8px}
.abstract-box p{margin:0}
.pdf-frame{height:calc(100vh - 60px)}
.pdf-frame object{width:100%;height:100%;border:0;display:block}
#transcripcion{padding:14px 16px;border-bottom:1px solid #d9e1e8;background:#fff}
</style>
</head>
<body>
<div class="viewer-head">
    <a href="./?idioma=<?php echo h($idioma); ?>"><?php echo h($project_name); ?></a>
    <div class="viewer-title"><?php echo h($titulo_doc); ?></div>
    <?php if ($texto_md): ?>
    <div class="voice-controls">
        <button id="btnPlay" onclick="leerTexto()">Reproducir</button>
        <button id="btnPause" onclick="pausarReanudarTexto()">Pausar/Reanudar</button>
        <button id="btnStop" onclick="detenerTexto()">Detener</button>
    </div>
    <?php endif; ?>
</div>

<?php if ($image_doc !== ''): ?>
<figure class="doc-image">
    <img src="<?php echo h(str_replace('%2F', '/', rawurlencode($image_doc))); ?>" alt="<?php echo h($titulo_doc); ?>">
</figure>
<?php endif; ?>

<?php if ($abstract_doc !== ''): ?>
<section class="abstract-box">
    <h2><?php echo h(menu_text($menu, 'abstract', $idioma)); ?></h2>
    <p><?php echo nl2br(h($abstract_doc)); ?></p>
</section>
<?php endif; ?>

<?php if ($texto_md): ?>
<div id="transcripcion"></div>
<script>
document.addEventListener("DOMContentLoaded", () => {
    inicializarLectura(<?php echo json_encode($texto_md, JSON_UNESCAPED_UNICODE); ?>, "<?php echo h($idioma_js); ?>");
});
</script>
<?php endif; ?>

<div class="pdf-frame">
    <object data="<?php echo h($pdf_directo); ?>" type="application/pdf">
        <p><a href="<?php echo h($pdf_directo); ?>" target="_blank">Descargar PDF</a></p>
    </object>
</div>
</body>
</html>
<?php
    exit;
}
?>
<!doctype html>
<html lang="<?php echo h($idioma); ?>">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?php echo h($project_name . ' - ' . $title_text); ?></title>
<link rel="stylesheet" href="/css/catalogo.css">
<style>
body{font-family:Arial,Helvetica,sans-serif;margin:0;color:#17202a;background:#fff}
.wrap{max-width:1100px;margin:0 auto;padding:28px 16px 44px}
.topbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;border-bottom:1px solid #d9e1e8;padding-bottom:16px;margin-bottom:18px}
.topbar a,.pill{display:inline-flex;align-items:center;justify-content:center;min-height:36px;padding:8px 12px;border:1px solid #d9e1e8;border-radius:6px;text-decoration:none;color:#0f6674;background:#fff;font-weight:700}
.pill.flag-pill{width:44px;padding:3px}
.pill.active{background:#0f6674;color:#fff;border-color:#0f6674}
h1{font-size:30px;line-height:1.15;margin:0 0 14px}
.note{background:#fff8ed;border-left:4px solid #8a5a00;padding:12px 14px;margin:16px 0 22px}
.grid{display:grid;gap:12px}
.card{border:1px solid #d9e1e8;border-radius:8px;padding:15px;background:#f7f9fb}
.card h2{font-size:18px;margin:0 0 10px}
.actions{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.button{display:inline-flex;align-items:center;min-height:36px;padding:8px 12px;border-radius:6px;background:#0f6674;color:#fff;text-decoration:none;font-weight:700}
.reader-button{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:6px;border:1px solid #0f6674;background:#fff;color:#0f6674;text-decoration:none;font-size:18px;font-weight:700}
.audio-icon{width:20px;height:20px;object-fit:contain;display:block}
.lang{display:inline-flex;align-items:center;min-height:30px;padding:5px 9px;border:1px solid #d9e1e8;border-radius:6px;color:#0f6674;text-decoration:none;background:#fff}
.flag{width:36px;height:25px;object-fit:cover;margin-right:6px;border:1px solid #d9e1e8;border-radius:2px}
.flag.only{margin-right:0}
.muted{color:#60707c}
</style>
</head>
<body id="top">
<main class="wrap">
    <h1><?php echo h($project_name); ?></h1>

    <nav class="topbar" aria-label="Navigation">
        <a href="https://estradad.es"><?php echo h(menu_text($menu, 'home', $idioma)); ?></a>
        <a href="/teorias/pdf/"><?php echo h(menu_text($menu, 'projects', $idioma)); ?></a>
        <a href="/catalogo.php"><?php echo h(menu_text($menu, 'catalog', $idioma)); ?></a>
        <?php foreach ($idiomas_soportados as $lang): ?>
            <?php $lang_has_flag = language_has_flag($lang); ?>
            <a class="pill <?php echo $lang_has_flag ? 'flag-pill ' : ''; ?><?php echo $idioma === $lang ? 'active' : ''; ?>" href="?idioma=<?php echo h($lang); ?><?php echo $mostrar_otros ? '&otros=1' : ''; ?>" aria-label="<?php echo h(language_label($lang)); ?>" title="<?php echo h(language_label($lang)); ?>">
                <?php echo language_button_content($lang); ?>
            </a>
        <?php endforeach; ?>
    </nav>

    <?php project_subdirectories_nav(__DIR__, $idioma); ?>

    <nav class="topbar" aria-label="Sections">
        <a class="pill <?php echo !$mostrar_otros ? 'active' : ''; ?>" href="?idioma=<?php echo h($idioma); ?>"><?php echo h(menu_text($menu, 'numbered', $idioma)); ?></a>
        <a class="pill <?php echo $mostrar_otros ? 'active' : ''; ?>" href="?idioma=<?php echo h($idioma); ?>&otros=1"><?php echo h(menu_text($menu, 'others', $idioma)); ?></a>
    </nav>

    <section class="grid">
    <?php if (!$mostrar_otros): ?>
    <?php foreach ($docs as $doc): ?>
        <?php
            $main_lang = best_lang_for_doc($doc, $idioma);
            if ($main_lang === null) {
                continue;
            }
            $main_pdf = $doc['files'][$main_lang]['pdf'];
            $title = title_for_doc($doc, $cat['rows'], $idioma);
            $open_url = open_url_for_pdf($dir, $main_pdf);
            $reader_url = reader_url_for_pdf($main_pdf);
            $has_md = md_exists_for_pdf($dir, $main_pdf);
            $show_request = $idioma !== 'es' && !doc_has_lang($doc, $idioma);
        ?>
        <article class="card">
            <h2><?php echo h($doc['id'] . ' - ' . $title); ?></h2>
            <div class="actions">
                <?php if ($main_pdf): ?>
                    <?php if ($has_md): ?>
                        <a class="reader-button" href="<?php echo h($reader_url); ?>" aria-label="Audio" title="Audio"><?php echo audio_button_content(); ?></a>
                    <?php endif; ?>
                    <a class="button" href="<?php echo h($open_url); ?>"><?php echo h(menu_text($menu, 'open', $idioma)); ?> <?php echo h(display_lang_code($main_lang)); ?></a>
                    <?php if ($show_request): ?>
                        <a class="lang" href="<?php echo h(translation_request_url($idioma, $main_pdf)); ?>"><?php echo h(menu_text($menu, 'request', $idioma)); ?> <?php echo strtoupper(h($idioma)); ?></a>
                    <?php endif; ?>
                <?php endif; ?>
            </div>
        </article>
    <?php endforeach; ?>
    <?php else: ?>
    <?php foreach ($otros as $item): ?>
        <?php
            $main_lang = best_lang_for_other($item, $idioma);
            if ($main_lang === null) {
                continue;
            }
            $main_pdf = $item['files'][$main_lang];
            $title = title_for_other($item, $idioma);
            $open_url = open_url_for_pdf($dir, $main_pdf);
            $reader_url = reader_url_for_pdf($main_pdf);
            $has_md = md_exists_for_pdf($dir, $main_pdf);
            $show_request = $idioma !== 'es' && !other_has_lang($item, $idioma);
        ?>
        <article class="card">
            <h2><?php echo h($title); ?></h2>
            <div class="actions">
                <?php if ($has_md): ?>
                    <a class="reader-button" href="<?php echo h($reader_url); ?>" aria-label="Audio" title="Audio"><?php echo audio_button_content(); ?></a>
                <?php endif; ?>
                <a class="button" href="<?php echo h($open_url); ?>"><?php echo h(menu_text($menu, 'open', $idioma)); ?> <?php echo h(display_lang_code($main_lang)); ?></a>
                <?php if ($show_request): ?>
                    <a class="lang" href="<?php echo h(translation_request_url($idioma, $main_pdf)); ?>"><?php echo h(menu_text($menu, 'request', $idioma)); ?> <?php echo strtoupper(h($idioma)); ?></a>
                <?php endif; ?>
            </div>
        </article>
    <?php endforeach; ?>
    <?php endif; ?>
    </section>

    <p style="margin-top:24px"><a href="#top"><?php echo h(menu_text($menu, 'top', $idioma)); ?></a></p>
</main>
</body>
</html>
