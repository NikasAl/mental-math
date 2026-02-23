# Лежандр — Camera & Image Processing
## Спецификация работы с камерой и изображениями

---

## 1. Обзор использования камеры

### 1.1 Сценарии использования

| Сценарий | Категория | Описание |
|----------|-----------|----------|
| Фото условия задачи | `condition` | Снимок условия из учебника/экрана |
| Фото решения | `solution` | Снимок рукописного решения |
| Фото озарения | `epiphany` | Схема/набросок при озарении |
| Фото контекста вопроса | `question` | Фрагмент для пояснения вопроса |
| Фото контекста подсказки | `hint` | Фрагмент для пояснения проблемы |

### 1.2 Пользовательский флоу

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAMERA CAPTURE FLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. TRIGGER (из разных мест)                                   │
│     ├── Problem Detail → 📷 Фото условия                        │
│     ├── Session → 📷 Фото решения                               │
│     ├── Epiphany → 📷 Фото схемы                                │
│     ├── Question → 📷 Фото контекста                            │
│     └── Hint → 📷 Фото контекста                                │
│                                                                 │
│  2. CAPTURE                                                     │
│     ├── Камера: Снимок → Превью → Подтверждение                │
│     └── Галерея: Выбор → Превью → Подтверждение                │
│                                                                 │
│  3. PROCESSING                                                  │
│     ├── Загрузка на сервер (upload)                            │
│     ├── Опционально: OCR распознавание                         │
│     └── Отображение результата                                  │
│                                                                 │
│  4. RESULT                                                      │
│     ├── Изображение сохранено                                   │
│     ├── Текст распознан (если OCR)                             │
│     └── Готово к редактированию                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Архитектура камеры

### 2.1 Зависимости

```yaml
# pubspec.yaml
dependencies:
  # Camera access
  camera: ^0.10.5+9
  
  # Image picker (gallery)
  image_picker: ^1.0.7
  
  # Image processing
  image: ^4.1.7
  
  # Path provider for temp files
  path_provider: ^2.1.2
  
  # Permissions
  permission_handler: ^11.3.0
```

### 2.2 Camera Service

```dart
// lib/core/services/camera_service.dart

import 'dart:io';
import 'package:camera/camera.dart';
import 'package:flutter/foundation.dart';
import 'package:image_picker/image_picker.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:path_provider/path_provider.dart';
import 'package:image/image.dart' as img;

enum CaptureSource { camera, gallery }

class CaptureResult {
  final String filePath;
  final int? width;
  final int? height;
  final int? fileSizeBytes;

  CaptureResult({
    required this.filePath,
    this.width,
    this.height,
    this.fileSizeBytes,
  });
}

class CameraService {
  final ImagePicker _imagePicker = ImagePicker();
  List<CameraDescription>? _cameras;
  bool _isInitialized = false;

  Future<void> initialize() async {
    if (_isInitialized) return;
    
    _cameras = await availableCameras();
    _isInitialized = true;
  }

  Future<bool> requestPermissions() async {
    final cameraStatus = await Permission.camera.request();
    final storageStatus = await Permission.storage.request();
    final photosStatus = await Permission.photos.request();
    
    return cameraStatus.isGranted && 
           (storageStatus.isGranted || photosStatus.isGranted);
  }

  Future<CaptureResult?> captureFromCamera({
    CameraLensDirection lens = CameraLensDirection.back,
    int imageQuality = 85,
    int? maxWidth,
    int? maxHeight,
  }) async {
    if (!await requestPermissions()) {
      throw CameraException('PERMISSION_DENIED', 'Camera permission denied');
    }

    final XFile? image = await _imagePicker.pickImage(
      source: ImageSource.camera,
      preferredCameraDevice: lens == CameraLensDirection.back
          ? CameraDevice.rear
          : CameraDevice.front,
      imageQuality: imageQuality,
      maxWidth: maxWidth?.toDouble(),
      maxHeight: maxHeight?.toDouble(),
    );

    if (image == null) return null;

    return CaptureResult(
      filePath: image.path,
      fileSizeBytes: await image.length(),
    );
  }

  Future<CaptureResult?> captureFromGallery({
    int imageQuality = 85,
    int? maxWidth,
    int? maxHeight,
  }) async {
    final XFile? image = await _imagePicker.pickImage(
      source: ImageSource.gallery,
      imageQuality: imageQuality,
      maxWidth: maxWidth?.toDouble(),
      maxHeight: maxHeight?.toDouble(),
    );

    if (image == null) return null;

    return CaptureResult(
      filePath: image.path,
      fileSizeBytes: await image.length(),
    );
  }

  Future<CaptureResult?> capture({
    CaptureSource source = CaptureSource.camera,
    CameraLensDirection lens = CameraLensDirection.back,
    int imageQuality = 85,
    int? maxWidth,
    int? maxHeight,
  }) async {
    if (source == CaptureSource.camera) {
      return await captureFromCamera(
        lens: lens,
        imageQuality: imageQuality,
        maxWidth: maxWidth,
        maxHeight: maxHeight,
      );
    } else {
      return await captureFromGallery(
        imageQuality: imageQuality,
        maxWidth: maxWidth,
        maxHeight: maxHeight,
      );
    }
  }

  List<CameraDescription> get cameras => _cameras ?? [];
  
  bool get isInitialized => _isInitialized;
}
```

### 2.3 Image Compression Service

```dart
// lib/core/services/image_compression_service.dart

import 'dart:io';
import 'package:image/image.dart' as img;
import 'package:path_provider/path_provider.dart';

class CompressionResult {
  final String filePath;
  final int originalSize;
  final int compressedSize;
  final int width;
  final int height;

  CompressionResult({
    required this.filePath,
    required this.originalSize,
    required this.compressedSize,
    required this.width,
    required this.height,
  });

  double get compressionRatio => 
      originalSize > 0 ? compressedSize / originalSize : 0;
}

class ImageCompressionService {
  /// Максимальная ширина изображения
  static const int defaultMaxWidth = 1920;
  
  /// Максимальная высота изображения
  static const int defaultMaxHeight = 1920;
  
  /// Качество JPEG (0-100)
  static const int defaultQuality = 85;

  Future<CompressionResult> compress({
    required String inputPath,
    int maxWidth = defaultMaxWidth,
    int maxHeight = defaultMaxHeight,
    int quality = defaultQuality,
  }) async {
    final inputFile = File(inputPath);
    final originalBytes = await inputFile.readAsBytes();
    final originalSize = originalBytes.length;

    // Decode image
    final image = img.decodeImage(originalBytes);
    if (image == null) {
      throw Exception('Failed to decode image');
    }

    // Resize if needed
    img.Image resized = image;
    if (image.width > maxWidth || image.height > maxHeight) {
      resized = img.copyResize(
        image,
        width: maxWidth,
        height: maxHeight,
        interpolation: img.Interpolation.linear,
        maintainAspect: true,
      );
    }

    // Encode as JPEG
    final compressedBytes = img.encodeJpg(resized, quality: quality);

    // Save to temp file
    final tempDir = await getTemporaryDirectory();
    final fileName = 'compressed_${DateTime.now().millisecondsSinceEpoch}.jpg';
    final outputPath = '${tempDir.path}/$fileName';
    
    await File(outputPath).writeAsBytes(compressedBytes);

    return CompressionResult(
      filePath: outputPath,
      originalSize: originalSize,
      compressedSize: compressedBytes.length,
      width: resized.width,
      height: resized.height,
    );
  }

  /// Создаёт превью изображение для быстрого отображения
  Future<String> createThumbnail({
    required String inputPath,
    int size = 200,
    int quality = 70,
  }) async {
    final inputFile = File(inputPath);
    final bytes = await inputFile.readAsBytes();

    final image = img.decodeImage(bytes);
    if (image == null) {
      throw Exception('Failed to decode image');
    }

    final thumbnail = img.copyResize(
      image,
      width: size,
      height: size,
      interpolation: img.Interpolation.linear,
      maintainAspect: true,
    );

    final thumbnailBytes = img.encodeJpg(thumbnail, quality: quality);

    final tempDir = await getTemporaryDirectory();
    final fileName = 'thumb_${DateTime.now().millisecondsSinceEpoch}.jpg';
    final outputPath = '${tempDir.path}/$fileName';
    
    await File(outputPath).writeAsBytes(thumbnailBytes);

    return outputPath;
  }
}
```

---

## 3. Camera Screen Implementation

### 3.1 Camera Screen

```dart
// lib/presentation/screens/camera/camera_screen.dart

import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:camera/camera.dart';
import '../../../core/services/camera_service.dart';
import '../../../data/services/upload_service.dart';

enum ImageCategory {
  condition('Условие задачи'),
  solution('Решение'),
  epiphany('Схема озарения'),
  question('Контекст вопроса'),
  hint('Контекст подсказки');

  final String label;
  const ImageCategory(this.label);
}

class CameraScreen extends ConsumerStatefulWidget {
  final ImageCategory category;
  final int entityId;
  final Function(String imagePath)? onImageCaptured;

  const CameraScreen({
    super.key,
    required this.category,
    required this.entityId,
    this.onImageCaptured,
  });

  @override
  ConsumerState<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends ConsumerState<CameraScreen> {
  final CameraService _cameraService = CameraService();
  CameraController? _cameraController;
  bool _isInitializing = true;
  bool _isCapturing = false;
  String? _capturedImagePath;
  int _selectedCameraIndex = 0;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    try {
      await _cameraService.initialize();
      final cameras = _cameraService.cameras;
      
      if (cameras.isNotEmpty) {
        // Find back camera by default
        final backCameraIndex = cameras.indexWhere(
          (c) => c.lensDirection == CameraLensDirection.back,
        );
        _selectedCameraIndex = backCameraIndex >= 0 ? backCameraIndex : 0;
        
        _cameraController = CameraController(
          cameras[_selectedCameraIndex],
          ResolutionPreset.high,
          enableAudio: false,
          imageFormatGroup: ImageFormatGroup.jpeg,
        );
        
        await _cameraController!.initialize();
      }
    } catch (e) {
      debugPrint('Camera init error: $e');
    } finally {
      setState(() => _isInitializing = false);
    }
  }

  Future<void> _takePicture() async {
    if (_cameraController == null || !_cameraController!.value.isInitialized) {
      return;
    }

    setState(() => _isCapturing = true);

    try {
      final image = await _cameraController!.takePicture();
      setState(() {
        _capturedImagePath = image.path;
        _isCapturing = false;
      });
    } catch (e) {
      debugPrint('Capture error: $e');
      setState(() => _isCapturing = false);
    }
  }

  Future<void> _switchCamera() async {
    final cameras = _cameraService.cameras;
    if (cameras.length < 2) return;

    setState(() => _isInitializing = true);

    await _cameraController?.dispose();
    
    _selectedCameraIndex = (_selectedCameraIndex + 1) % cameras.length;
    
    _cameraController = CameraController(
      cameras[_selectedCameraIndex],
      ResolutionPreset.high,
      enableAudio: false,
    );
    
    await _cameraController!.initialize();
    
    setState(() => _isInitializing = false);
  }

  void _retake() {
    setState(() => _capturedImagePath = null);
  }

  Future<void> _confirmAndUpload() async {
    if (_capturedImagePath == null) return;

    final uploadService = ref.read(uploadServiceProvider);

    // Show loading
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => const Center(child: CircularProgressIndicator()),
    );

    try {
      final success = await uploadService.uploadImage(
        category: _mapCategory(widget.category),
        entityId: widget.entityId,
        filePath: _capturedImagePath!,
      );

      Navigator.pop(context); // Hide loading

      if (success) {
        widget.onImageCaptured?.call(_capturedImagePath!);
        if (mounted) Navigator.pop(context, _capturedImagePath);
      } else {
        _showError('Не удалось загрузить изображение');
      }
    } catch (e) {
      Navigator.pop(context);
      _showError('Ошибка: $e');
    }
  }

  UploadCategory _mapCategory(ImageCategory cat) {
    switch (cat) {
      case ImageCategory.condition:
        return UploadCategory.condition;
      case ImageCategory.solution:
        return UploadCategory.solution;
      case ImageCategory.epiphany:
        return UploadCategory.epiphany;
      case ImageCategory.question:
        return UploadCategory.question;
      case ImageCategory.hint:
        return UploadCategory.hint;
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), backgroundColor: Colors.red),
    );
  }

  Future<void> _pickFromGallery() async {
    final result = await _cameraService.captureFromGallery();
    if (result != null) {
      setState(() => _capturedImagePath = result.filePath);
    }
  }

  @override
  void dispose() {
    _cameraController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.close, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          widget.category.label,
          style: const TextStyle(color: Colors.white),
        ),
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_isInitializing) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(color: Colors.white),
            SizedBox(height: 16),
            Text('Инициализация камеры...', style: TextStyle(color: Colors.white)),
          ],
        ),
      );
    }

    if (_capturedImagePath != null) {
      return _buildPreview();
    }

    return _buildCameraView();
  }

  Widget _buildCameraView() {
    if (_cameraController == null || !_cameraController!.value.isInitialized) {
      return const Center(
        child: Text(
          'Камера недоступна',
          style: TextStyle(color: Colors.white),
        ),
      );
    }

    return Column(
      children: [
        Expanded(
          child: Stack(
            fit: StackFit.expand,
            children: [
              CameraPreview(_cameraController!),
              // Guide overlay
              _buildGuideOverlay(),
            ],
          ),
        ),
        _buildControls(),
      ],
    );
  }

  Widget _buildGuideOverlay() {
    return Positioned.fill(
      child: CustomPaint(
        painter: _GuideOverlayPainter(),
      ),
    );
  }

  Widget _buildControls() {
    return Container(
      padding: const EdgeInsets.all(24),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          // Gallery
          IconButton(
            onPressed: _pickFromGallery,
            icon: const Icon(Icons.photo_library, color: Colors.white, size: 32),
          ),
          
          // Capture
          GestureDetector(
            onTap: _isCapturing ? null : _takePicture,
            child: Container(
              width: 72,
              height: 72,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                border: Border.all(color: Colors.white, width: 4),
              ),
              child: _isCapturing
                  ? const Center(
                      child: CircularProgressIndicator(color: Colors.white),
                    )
                  : const Icon(Icons.camera_alt, color: Colors.white, size: 32),
            ),
          ),
          
          // Switch camera
          IconButton(
            onPressed: _switchCamera,
            icon: const Icon(Icons.flip_camera_ios, color: Colors.white, size: 32),
          ),
        ],
      ),
    );
  }

  Widget _buildPreview() {
    return Column(
      children: [
        Expanded(
          child: InteractiveViewer(
            child: Image.file(
              File(_capturedImagePath!),
              fit: BoxFit.contain,
            ),
          ),
        ),
        Container(
          padding: const EdgeInsets.all(24),
          child: Column(
            children: [
              Text(
                widget.category.label,
                style: const TextStyle(color: Colors.white, fontSize: 16),
              ),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  TextButton.icon(
                    onPressed: _retake,
                    icon: const Icon(Icons.refresh, color: Colors.white),
                    label: const Text('Переснять', style: TextStyle(color: Colors.white)),
                  ),
                  ElevatedButton.icon(
                    onPressed: _confirmAndUpload,
                    icon: const Icon(Icons.check),
                    label: const Text('Отправить'),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ],
    );
  }
}

class _GuideOverlayPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.white.withOpacity(0.3)
      ..strokeWidth = 1
      ..style = PaintingStyle.stroke;

    // Draw document guide rectangle
    const padding = 32.0;
    final rect = Rect.fromLTWH(
      padding,
      padding,
      size.width - padding * 2,
      size.height - padding * 2,
    );

    // Draw corners only
    const cornerLength = 24.0;
    final path = Path();
    
    // Top-left
    path.moveTo(rect.left, rect.top + cornerLength);
    path.lineTo(rect.left, rect.top);
    path.lineTo(rect.left + cornerLength, rect.top);
    
    // Top-right
    path.moveTo(rect.right - cornerLength, rect.top);
    path.lineTo(rect.right, rect.top);
    path.lineTo(rect.right, rect.top + cornerLength);
    
    // Bottom-right
    path.moveTo(rect.right, rect.bottom - cornerLength);
    path.lineTo(rect.right, rect.bottom);
    path.lineTo(rect.right - cornerLength, rect.bottom);
    
    // Bottom-left
    path.moveTo(rect.left + cornerLength, rect.bottom);
    path.lineTo(rect.left, rect.bottom);
    path.lineTo(rect.left, rect.bottom - cornerLength);

    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
```

### 3.2 Camera Bottom Sheet

```dart
// lib/presentation/widgets/camera_bottom_sheet.dart

import 'dart:io';
import 'package:flutter/material.dart';
import 'camera_screen.dart';
import '../../../core/services/camera_service.dart';

class CameraBottomSheet extends StatelessWidget {
  final ImageCategory category;
  final int entityId;
  final Function(String imagePath)? onImageCaptured;

  const CameraBottomSheet({
    super.key,
    required this.category,
    required this.entityId,
    this.onImageCaptured,
  });

  static Future<String?> show({
    required BuildContext context,
    required ImageCategory category,
    required int entityId,
  }) async {
    return await showModalBottomSheet<String>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => CameraBottomSheet(
        category: category,
        entityId: entityId,
      ),
    );
  }

  Future<void> _openCamera(BuildContext context) async {
    final result = await Navigator.push<String>(
      context,
      MaterialPageRoute(
        builder: (context) => CameraScreen(
          category: category,
          entityId: entityId,
          onImageCaptured: onImageCaptured,
        ),
      ),
    );
    
    if (result != null && context.mounted) {
      Navigator.pop(context, result);
    }
  }

  Future<void> _pickFromGallery(BuildContext context) async {
    final cameraService = CameraService();
    final result = await cameraService.captureFromGallery();
    
    if (result != null && context.mounted) {
      Navigator.pop(context, result.filePath);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // Handle
              Container(
                width: 40,
                height: 4,
                decoration: BoxDecoration(
                  color: Colors.grey[300],
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
              const SizedBox(height: 24),
              
              Text(
                'Добавить изображение',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 8),
              Text(
                category.label,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: Colors.grey[600],
                ),
              ),
              const SizedBox(height: 24),
              
              // Options
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  _buildOption(
                    context,
                    icon: Icons.camera_alt,
                    label: 'Камера',
                    onTap: () => _openCamera(context),
                  ),
                  _buildOption(
                    context,
                    icon: Icons.photo_library,
                    label: 'Галерея',
                    onTap: () => _pickFromGallery(context),
                  ),
                ],
              ),
              
              const SizedBox(height: 24),
              
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('Отмена'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildOption(
    BuildContext context, {
    required IconData icon,
    required String label,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        width: 120,
        height: 120,
        decoration: BoxDecoration(
          border: Border.all(color: Colors.grey[300]!),
          borderRadius: BorderRadius.circular(16),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 48, color: Theme.of(context).primaryColor),
            const SizedBox(height: 8),
            Text(label),
          ],
        ),
      ),
    );
  }
}
```

---

## 4. OCR Integration

### 4.1 OCR Flow Widget

```dart
// lib/presentation/widgets/ocr_flow_widget.dart

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../data/repositories/artifacts_repository.dart';
import 'persona_selector.dart';

enum OcrTarget { problem, solution }

class OcrResult {
  final String text;
  final bool success;
  final String? error;

  OcrResult({
    required this.text,
    required this.success,
    this.error,
  });
}

class OcrFlowWidget extends ConsumerStatefulWidget {
  final OcrTarget target;
  final int entityId;
  final String? currentText;
  final Function(String text)? onOcrComplete;

  const OcrFlowWidget({
    super.key,
    required this.target,
    required this.entityId,
    this.currentText,
    this.onOcrComplete,
  });

  @override
  ConsumerState<OcrFlowWidget> createState() => _OcrFlowWidgetState();
}

class _OcrFlowWidgetState extends ConsumerState<OcrFlowWidget> {
  bool _isProcessing = false;
  String? _recognizedText;
  String? _error;

  Future<void> _startOcr(String persona) async {
    setState(() {
      _isProcessing = true;
      _error = null;
    });

    try {
      final repo = ref.read(artifactsRepositoryProvider);
      
      String text;
      if (widget.target == OcrTarget.problem) {
        text = await repo.triggerProblemOcr(widget.entityId, persona);
      } else {
        text = await repo.triggerSolutionOcr(widget.entityId, persona);
      }

      setState(() {
        _recognizedText = text;
        _isProcessing = false;
      });

      widget.onOcrComplete?.call(text);
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isProcessing = false;
      });
    }
  }

  void _showPersonaSelector() {
    PersonaSelector.show(
      context: context,
      title: 'Распознавание текста',
      subtitle: 'Выберите AI для распознавания',
      onSelected: (persona) {
        _startOcr(persona.id);
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_isProcessing) {
      return _buildProcessing();
    }

    if (_error != null) {
      return _buildError();
    }

    if (_recognizedText != null) {
      return _buildResult();
    }

    return _buildInitial();
  }

  Widget _buildInitial() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.auto_awesome, size: 20),
                const SizedBox(width: 8),
                Text(
                  'AI Распознавание',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              'Преобразовать изображение в текст с формулами',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: Colors.grey[600],
              ),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: _showPersonaSelector,
                icon: const Icon(Icons.document_scanner),
                label: const Text('Распознать (OCR)'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildProcessing() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            const CircularProgressIndicator(),
            const SizedBox(height: 16),
            Text(
              'Распознавание текста...',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 8),
            Text(
              'Это может занять несколько секунд',
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                color: Colors.grey[600],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildError() {
    return Card(
      color: Colors.red[50],
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Icon(Icons.error_outline, color: Colors.red),
            const SizedBox(height: 8),
            Text(
              'Ошибка распознавания',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                color: Colors.red,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              _error ?? 'Неизвестная ошибка',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _showPersonaSelector,
              child: const Text('Попробовать снова'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildResult() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.check_circle, color: Colors.green, size: 20),
                const SizedBox(width: 8),
                Text(
                  'Текст распознан',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    color: Colors.green,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Container(
              constraints: const BoxConstraints(maxHeight: 200),
              child: SingleChildScrollView(
                child: SelectableText(
                  _recognizedText ?? '',
                  style: const TextStyle(fontFamily: 'monospace'),
                ),
              ),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                TextButton(
                  onPressed: _showPersonaSelector,
                  child: const Text('Перераспознать'),
                ),
                const SizedBox(width: 8),
                ElevatedButton(
                  onPressed: () {
                    // Edit text in markdown viewer
                  },
                  child: const Text('Редактировать'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## 5. Image Display Components

### 5.1 Cached Image Widget

```dart
// lib/presentation/widgets/cached_image_widget.dart

import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';

class CachedImageWidget extends StatelessWidget {
  final String? imageUrl;
  final String? localPath;
  final double? width;
  final double? height;
  final BoxFit fit;
  final BorderRadius? borderRadius;
  final Widget? placeholder;
  final Widget? errorWidget;

  const CachedImageWidget({
    super.key,
    this.imageUrl,
    this.localPath,
    this.width,
    this.height,
    this.fit = BoxFit.cover,
    this.borderRadius,
    this.placeholder,
    this.errorWidget,
  });

  @override
  Widget build(BuildContext context) {
    Widget image;

    if (localPath != null) {
      image = Image.file(
        File(localPath!),
        width: width,
        height: height,
        fit: fit,
        errorBuilder: (_, __, ___) => _buildError(),
      );
    } else if (imageUrl != null && imageUrl!.isNotEmpty) {
      image = CachedNetworkImage(
        imageUrl: _getFullUrl(imageUrl!),
        width: width,
        height: height,
        fit: fit,
        placeholder: (_, __) => placeholder ?? _buildPlaceholder(),
        errorWidget: (_, __, ___) => errorWidget ?? _buildError(),
      );
    } else {
      image = errorWidget ?? _buildError();
    }

    if (borderRadius != null) {
      image = ClipRRect(borderRadius: borderRadius!, child: image);
    }

    return image;
  }

  String _getFullUrl(String path) {
    if (path.startsWith('http')) return path;
    return '${AppConfig.apiBaseUrl}$path';
  }

  Widget _buildPlaceholder() {
    return Container(
      width: width,
      height: height,
      color: Colors.grey[200],
      child: const Center(
        child: CircularProgressIndicator(strokeWidth: 2),
      ),
    );
  }

  Widget _buildError() {
    return Container(
      width: width,
      height: height,
      color: Colors.grey[200],
      child: Icon(
        Icons.broken_image,
        color: Colors.grey[400],
        size: 48,
      ),
    );
  }
}
```

### 5.2 Fullscreen Image Viewer

```dart
// lib/presentation/widgets/fullscreen_image_viewer.dart

import 'dart:io';
import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';

class FullscreenImageViewer extends StatefulWidget {
  final String? imageUrl;
  final String? localPath;
  final String? title;

  const FullscreenImageViewer({
    super.key,
    this.imageUrl,
    this.localPath,
    this.title,
  });

  static Future<void> show({
    required BuildContext context,
    String? imageUrl,
    String? localPath,
    String? title,
  }) {
    return Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => FullscreenImageViewer(
          imageUrl: imageUrl,
          localPath: localPath,
          title: title,
        ),
      ),
    );
  }

  @override
  State<FullscreenImageViewer> createState() => _FullscreenImageViewerState();
}

class _FullscreenImageViewerState extends State<FullscreenImageViewer> {
  final TransformationController _transformController = TransformationController();

  @override
  void dispose() {
    _transformController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: widget.title != null ? Text(widget.title!) : null,
        actions: [
          IconButton(
            icon: const Icon(Icons.zoom_out),
            onPressed: _zoomOut,
          ),
          IconButton(
            icon: const Icon(Icons.zoom_in),
            onPressed: _zoomIn,
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _resetZoom,
          ),
        ],
      ),
      body: GestureDetector(
        onDoubleTap: _resetZoom,
        child: InteractiveViewer(
          transformationController: _transformController,
          minScale: 0.5,
          maxScale: 4.0,
          child: Center(
            child: _buildImage(),
          ),
        ),
      ),
    );
  }

  Widget _buildImage() {
    if (widget.localPath != null) {
      return Image.file(
        File(widget.localPath!),
        fit: BoxFit.contain,
      );
    } else if (widget.imageUrl != null) {
      return CachedNetworkImage(
        imageUrl: widget.imageUrl!,
        fit: BoxFit.contain,
        placeholder: (_, __) => const Center(
          child: CircularProgressIndicator(color: Colors.white),
        ),
        errorWidget: (_, __, ___) => const Center(
          child: Icon(Icons.error, color: Colors.white, size: 48),
        ),
      );
    }
    
    return const Center(
      child: Text('Нет изображения', style: TextStyle(color: Colors.white)),
    );
  }

  void _zoomIn() {
    final matrix = _transformController.value.clone();
    matrix.scale(1.2, 1.2, 1.0);
    _transformController.value = matrix;
  }

  void _zoomOut() {
    final matrix = _transformController.value.clone();
    matrix.scale(0.8, 0.8, 1.0);
    _transformController.value = matrix;
  }

  void _resetZoom() {
    _transformController.value = Matrix4.identity();
  }
}
```

---

## 6. Permissions Handling

```dart
// lib/core/services/permission_service.dart

import 'package:permission_handler/permission_handler.dart';

class PermissionService {
  Future<bool> requestCameraPermission() async {
    final status = await Permission.camera.request();
    return status.isGranted;
  }

  Future<bool> requestStoragePermission() async {
    // For Android 13+ use photos permission
    if (await Permission.photos.isGranted) {
      return true;
    }
    
    final status = await Permission.photos.request();
    if (status.isGranted) {
      return true;
    }
    
    // Fallback for older Android
    final storageStatus = await Permission.storage.request();
    return storageStatus.isGranted;
  }

  Future<bool> checkCameraPermission() async {
    final status = await Permission.camera.status;
    return status.isGranted;
  }

  Future<bool> checkStoragePermission() async {
    final photosStatus = await Permission.photos.status;
    if (photosStatus.isGranted) return true;
    
    final storageStatus = await Permission.storage.status;
    return storageStatus.isGranted;
  }

  Future<void> openAppSettings() async {
    await openAppSettings();
  }

  Future<Map<String, bool>> checkAllPermissions() async {
    return {
      'camera': await checkCameraPermission(),
      'storage': await checkStoragePermission(),
    };
  }
}
```

---

## 7. Platform-Specific Configuration

### 7.1 Android (android/app/src/main/AndroidManifest.xml)

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <!-- Camera -->
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-feature android:name="android.hardware.camera" />
    <uses-feature android:name="android.hardware.camera.autofocus" />
    
    <!-- Storage -->
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    
    <!-- Android 13+ Media -->
    <uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
    <uses-permission android:name="android.permission.READ_MEDIA_VIDEO" />
    
    <!-- Internet -->
    <uses-permission android:name="android.permission.INTERNET" />
    
    <application ...>
        <!-- FileProvider for camera images -->
        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
        </provider>
    </application>
</manifest>
```

### 7.2 iOS (ios/Runner/Info.plist)

```xml
<dict>
    <!-- Camera -->
    <key>NSCameraUsageDescription</key>
    <string>Приложение использует камеру для фотографирования условий и решений задач</string>
    
    <!-- Photo Library -->
    <key>NSPhotoLibraryUsageDescription</key>
    <string>Приложение использует галерею для загрузки изображений задач</string>
    
    <key>NSPhotoLibraryAddUsageDescription</key>
    <string>Приложение может сохранять изображения в галерею</string>
    
    <!-- Microphone (required by camera plugin even if not used) -->
    <key>NSMicrophoneUsageDescription</key>
    <string>Приложение не использует микрофон</string>
</dict>
```

### 7.3 File Paths (android/app/src/main/res/xml/file_paths.xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<paths>
    <external-path name="external_files" path="." />
    <cache-path name="cache" path="." />
    <files-path name="files" path="." />
</paths>
```

---

## 8. Summary

### Ключевые компоненты:

| Компонент | Назначение |
|-----------|------------|
| `CameraService` | Управление камерой и галереей |
| `ImageCompressionService` | Сжатие и оптимизация изображений |
| `CameraScreen` | Полноэкранный захват фото |
| `CameraBottomSheet` | Быстрый выбор источник |
| `OcrFlowWidget` | Процесс OCR распознавания |
| `CachedImageWidget` | Отображение с кешированием |
| `FullscreenImageViewer` | Просмотр с зумом |
| `PermissionService` | Управление разрешениями |

### Размеры изображений:

| Параметр | Значение |
|----------|----------|
| Максимальная ширина | 1920px |
| Максимальная высота | 1920px |
| Качество JPEG | 85% |
| Превью | 200px |

---

*Спецификация камеры и обработки изображений для Flutter приложения "Лежандр"*
