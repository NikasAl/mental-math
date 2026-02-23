# Лежандр — Flutter API Layer
## Спецификация API слоя

---

## 1. Архитектура Data Layer

```
data/
├── models/              # DTO (Data Transfer Objects)
│   ├── user.dart
│   ├── problem.dart
│   ├── solution.dart
│   ├── session.dart
│   ├── epiphany.dart
│   ├── question.dart
│   ├── hint.dart
│   ├── concept.dart
│   ├── source.dart
│   ├── tag.dart
│   ├── gamification.dart
│   ├── billing.dart
│   └── api_response.dart
│
├── services/
│   ├── api_client.dart          # Dio + Interceptors
│   ├── auth_service.dart        # Авторизация
│   └── upload_service.dart      # Загрузка файлов
│
├── repositories/
│   ├── auth_repository.dart
│   ├── problems_repository.dart
│   ├── solutions_repository.dart
│   ├── artifacts_repository.dart
│   ├── concepts_repository.dart
│   ├── billing_repository.dart
│   └── gamification_repository.dart
│
└── storage/
    ├── token_storage.dart       # SecureStorage
    └── device_storage.dart      # Device credentials
```

---

## 2. Models (DTO)

### 2.1 User

```dart
// lib/data/models/user.dart

import 'package:json_annotation/json_annotation.dart';

part 'user.g.dart';

enum UserRole { admin, moderator, user }

@JsonSerializable()
class UserModel {
  final int id;
  final String? email;
  final String username;
  final bool isAnonymous;
  final String? deviceId;
  final UserRole role;
  final DateTime createdAt;

  UserModel({
    required this.id,
    this.email,
    required this.username,
    required this.isAnonymous,
    this.deviceId,
    required this.role,
    required this.createdAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) => 
      _$UserModelFromJson(json);
  Map<String, dynamic> toJson() => _$UserModelToJson(this);
}

@JsonSerializable()
class AuthResponse {
  final String accessToken;
  final String tokenType;
  final UserModel user;

  AuthResponse({
    required this.accessToken,
    required this.tokenType,
    required this.user,
  });

  factory AuthResponse.fromJson(Map<String, dynamic> json) => 
      _$AuthResponseFromJson(json);
}
```

### 2.2 Problem

```dart
// lib/data/models/problem.dart

@JsonSerializable()
class SourceModel {
  final int id;
  final String name;
  final String slug;
  final String? urlTemplate;

  SourceModel({
    required this.id,
    required this.name,
    required this.slug,
    this.urlTemplate,
  });

  factory SourceModel.fromJson(Map<String, dynamic> json) => 
      _$SourceModelFromJson(json);
}

@JsonSerializable()
class TagModel {
  final int id;
  final String name;
  final String slug;

  TagModel({
    required this.id,
    required this.name,
    required this.slug,
  });

  factory TagModel.fromJson(Map<String, dynamic> json) => 
      _$TagModelFromJson(json);
}

@JsonSerializable()
class ProblemModel {
  final int id;
  final int sourceId;
  final String reference;
  final String? conditionText;
  final String? conditionImg;
  final DateTime createdAt;
  final SourceModel source;
  final List<TagModel> tags;
  final List<ProblemConceptModel>? concepts;

  ProblemModel({
    required this.id,
    required this.sourceId,
    required this.reference,
    this.conditionText,
    this.conditionImg,
    required this.createdAt,
    required this.source,
    required this.tags,
    this.concepts,
  });

  factory ProblemModel.fromJson(Map<String, dynamic> json) => 
      _$ProblemModelFromJson(json);
  
  bool get hasText => conditionText != null && conditionText!.isNotEmpty;
  bool get hasImage => conditionImg != null && conditionImg!.isNotEmpty;
}

@JsonSerializable()
class ProblemCreate {
  final String reference;
  final String sourceName;
  final List<String> tags;
  final String? conditionText;

  ProblemCreate({
    required this.reference,
    required this.sourceName,
    required this.tags,
    this.conditionText,
  });

  Map<String, dynamic> toJson() => _$ProblemCreateToJson(this);
}
```

### 2.3 Solution

```dart
// lib/data/models/solution.dart

enum SolutionStatus { active, completed, abandoned }

@JsonSerializable()
class SolutionModel {
  final int id;
  final int problemId;
  final int userId;
  final SolutionStatus status;
  final int? personalDifficulty;
  final double? qualityScore;
  final double? xpEarned;
  final String? userNotes;
  final String? solutionImgPath;
  final String? solutionText;
  final double totalMinutes;
  final DateTime createdAt;
  final ProblemModel? problem;

  SolutionModel({
    required this.id,
    required this.problemId,
    required this.userId,
    required this.status,
    this.personalDifficulty,
    this.qualityScore,
    this.xpEarned,
    this.userNotes,
    this.solutionImgPath,
    this.solutionText,
    required this.totalMinutes,
    required this.createdAt,
    this.problem,
  });

  factory SolutionModel.fromJson(Map<String, dynamic> json) => 
      _$SolutionModelFromJson(json);
  
  bool get hasText => solutionText != null && solutionText!.isNotEmpty;
  bool get hasImage => solutionImgPath != null && solutionImgPath!.isNotEmpty;
  bool get isActive => status == SolutionStatus.active;
  bool get isCompleted => status == SolutionStatus.completed;
}

@JsonSerializable()
class SolutionFinish {
  final String status;
  final int? personalDifficulty;
  final double? qualityScore;
  final String? userNotes;

  SolutionFinish({
    required this.status,
    this.personalDifficulty,
    this.qualityScore,
    this.userNotes,
  });

  Map<String, dynamic> toJson() => _$SolutionFinishToJson(this);
}
```

### 2.4 Session

```dart
// lib/data/models/session.dart

@JsonSerializable()
class SessionModel {
  final int id;
  final int solutionId;
  final DateTime startTime;
  final DateTime? endTime;
  final double? durationMinutes;
  final String? notes;

  SessionModel({
    required this.id,
    required this.solutionId,
    required this.startTime,
    this.endTime,
    this.durationMinutes,
    this.notes,
  });

  factory SessionModel.fromJson(Map<String, dynamic> json) => 
      _$SessionModelFromJson(json);
}

@JsonSerializable()
class SessionCreate {
  final int solutionId;
  final DateTime startTime;
  final DateTime endTime;
  final double duration;

  SessionCreate({
    required this.solutionId,
    required this.startTime,
    required this.endTime,
    required this.duration,
  });

  Map<String, dynamic> toJson() => _$SessionCreateToJson(this);
}
```

### 2.5 Epiphany

```dart
// lib/data/models/epiphany.dart

@JsonSerializable()
class EpiphanyModel {
  final int id;
  final int solutionId;
  final String description;
  final int strength;
  final DateTime createdAt;
  final String? imagePath;

  EpiphanyModel({
    required this.id,
    required this.solutionId,
    required this.description,
    required this.strength,
    required this.createdAt,
    this.imagePath,
  });

  factory EpiphanyModel.fromJson(Map<String, dynamic> json) => 
      _$EpiphanyModelFromJson(json);
}

@JsonSerializable()
class EpiphanyCreate {
  final int solutionId;
  final String description;
  final int magnitude;

  EpiphanyCreate({
    required this.solutionId,
    required this.description,
    required this.magnitude,
  });

  Map<String, dynamic> toJson() => _$EpiphanyCreateToJson(this);
}
```

### 2.6 Question

```dart
// lib/data/models/question.dart

@JsonSerializable()
class QuestionModel {
  final int id;
  final int solutionId;
  final String body;
  final String? answer;
  final bool isAnswered;
  final DateTime createdAt;
  final String? imagePath;

  QuestionModel({
    required this.id,
    required this.solutionId,
    required this.body,
    this.answer,
    required this.isAnswered,
    required this.createdAt,
    this.imagePath,
  });

  factory QuestionModel.fromJson(Map<String, dynamic> json) => 
      _$QuestionModelFromJson(json);
}

@JsonSerializable()
class QuestionCreate {
  final int solutionId;
  final String body;

  QuestionCreate({
    required this.solutionId,
    required this.body,
  });

  Map<String, dynamic> toJson() => _$QuestionCreateToJson(this);
}

@JsonSerializable()
class QuestionAnswer {
  final String answer;

  QuestionAnswer({required this.answer});

  Map<String, dynamic> toJson() => _$QuestionAnswerToJson(this);
}
```

### 2.7 Hint

```dart
// lib/data/models/hint.dart

enum HintStatus { draft, completed }

@JsonSerializable()
class HintModel {
  final int id;
  final int solutionId;
  final String? hintText;
  final String? userNotes;
  final String? aiModel;
  final HintStatus status;
  final DateTime createdAt;

  HintModel({
    required this.id,
    required this.solutionId,
    this.hintText,
    this.userNotes,
    this.aiModel,
    required this.status,
    required this.createdAt,
  });

  factory HintModel.fromJson(Map<String, dynamic> json) => 
      _$HintModelFromJson(json);
}

@JsonSerializable()
class HintDraftCreate {
  final int solutionId;
  final String? userNotes;

  HintDraftCreate({
    required this.solutionId,
    this.userNotes,
  });

  Map<String, dynamic> toJson() => _$HintDraftCreateToJson(this);
}
```

### 2.8 Concept

```dart
// lib/data/models/concept.dart

@JsonSerializable()
class ConceptModel {
  final int id;
  final String name;
  final String slug;
  final String? description;
  final String? utilityDescription;
  final DateTime createdAt;

  ConceptModel({
    required this.id,
    required this.name,
    required this.slug,
    this.description,
    this.utilityDescription,
    required this.createdAt,
  });

  factory ConceptModel.fromJson(Map<String, dynamic> json) => 
      _$ConceptModelFromJson(json);
}

@JsonSerializable()
class ProblemConceptModel {
  final int problemId;
  final int conceptId;
  final double relevance;
  final String? explanation;
  final ConceptModel concept;

  ProblemConceptModel({
    required this.problemId,
    required this.conceptId,
    required this.relevance,
    this.explanation,
    required this.concept,
  });

  factory ProblemConceptModel.fromJson(Map<String, dynamic> json) => 
      _$ProblemConceptModelFromJson(json);
}

@JsonSerializable()
class SolutionConceptModel {
  final int solutionId;
  final int conceptId;
  final String? usageContext;
  final ConceptModel concept;

  SolutionConceptModel({
    required this.solutionId,
    required this.conceptId,
    this.usageContext,
    required this.concept,
  });

  factory SolutionConceptModel.fromJson(Map<String, dynamic> json) => 
      _$SolutionConceptModelFromJson(json);
}
```

### 2.9 Gamification

```dart
// lib/data/models/gamification.dart

@JsonSerializable()
class GamificationModel {
  final int userId;
  final double totalXp;
  final int currentLevel;
  final int currentHearts;
  final int maxHearts;
  final int streakCurrent;
  final int streakMax;
  final int solvedTasksToday;
  final DateTime? lastActivityDate;

  GamificationModel({
    required this.userId,
    required this.totalXp,
    required this.currentLevel,
    required this.currentHearts,
    required this.maxHearts,
    required this.streakCurrent,
    required this.streakMax,
    required this.solvedTasksToday,
    this.lastActivityDate,
  });

  factory GamificationModel.fromJson(Map<String, dynamic> json) => 
      _$GamificationModelFromJson(json);
  
  double get xpProgress {
    // XP needed for next level
    final xpForCurrentLevel = currentLevel * 100;
    final xpForNextLevel = (currentLevel + 1) * 100;
    final xpInLevel = totalXp - xpForCurrentLevel;
    final xpNeeded = xpForNextLevel - xpForCurrentLevel;
    return xpInLevel / xpNeeded;
  }
}

@JsonSerializable()
class DailyActivityModel {
  final String date;
  final double xp;
  final double timeMinutes;
  final int tasksCount;

  DailyActivityModel({
    required this.date,
    required this.xp,
    required this.timeMinutes,
    required this.tasksCount,
  });

  factory DailyActivityModel.fromJson(Map<String, dynamic> json) => 
      _$DailyActivityModelFromJson(json);
}

@JsonSerializable()
class ActivityResponse {
  final List<DailyActivityModel> items;
  final double totalXp;
  final double totalTimeMinutes;
  final int totalTasks;

  ActivityResponse({
    required this.items,
    required this.totalXp,
    required this.totalTimeMinutes,
    required this.totalTasks,
  });

  factory ActivityResponse.fromJson(Map<String, dynamic> json) => 
      _$ActivityResponseFromJson(json);
}
```

### 2.10 Billing

```dart
// lib/data/models/billing.dart

@JsonSerializable()
class BillingBalanceModel {
  final double balance;
  final String currency;
  final int freeUsesLeft;
  final int totalDailyLimit;

  BillingBalanceModel({
    required this.balance,
    required this.currency,
    required this.freeUsesLeft,
    required this.totalDailyLimit,
  });

  factory BillingBalanceModel.fromJson(Map<String, dynamic> json) => 
      _$BillingBalanceModelFromJson(json);
}

@JsonSerializable()
class TopUpResponse {
  final String paymentUrl;
  final String paymentId;

  TopUpResponse({
    required this.paymentUrl,
    required this.paymentId,
  });

  factory TopUpResponse.fromJson(Map<String, dynamic> json) => 
      _$TopUpResponseFromJson(json);
}
```

### 2.11 API Response

```dart
// lib/data/models/api_response.dart

@JsonSerializable()
class OcrResponse {
  final String text;

  OcrResponse({required this.text});

  factory OcrResponse.fromJson(Map<String, dynamic> json) => 
      _$OcrResponseFromJson(json);
}

@JsonSerializable()
class ApiError {
  final String detail;
  final int? code;

  ApiError({required this.detail, this.code});

  factory ApiError.fromJson(Map<String, dynamic> json) => 
      _$ApiErrorFromJson(json);
}
```

---

## 3. Storage

### 3.1 Token Storage

```dart
// lib/data/storage/token_storage.dart

import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class TokenStorage {
  static const _accessTokenKey = 'access_token';
  static const _refreshTokenKey = 'refresh_token';
  
  final FlutterSecureStorage _storage;

  TokenStorage({FlutterSecureStorage? storage})
      : _storage = storage ?? const FlutterSecureStorage();

  Future<void> saveToken(String token) async {
    await _storage.write(key: _accessTokenKey, value: token);
  }

  Future<String?> getToken() async {
    return await _storage.read(key: _accessTokenKey);
  }

  Future<void> deleteToken() async {
    await _storage.delete(key: _accessTokenKey);
  }

  Future<bool> hasToken() async {
    final token = await getToken();
    return token != null && token.isNotEmpty;
  }
}
```

### 3.2 Device Storage

```dart
// lib/data/storage/device_storage.dart

import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:uuid/uuid.dart';
import 'package:crypto/crypto.dart';

class DeviceCredentials {
  final String deviceId;
  final String secretKey;

  DeviceCredentials({
    required this.deviceId,
    required this.secretKey,
  });

  Map<String, dynamic> toMap() => {
        'device_id': deviceId,
        'secret': secretKey,
      };

  factory DeviceCredentials.fromMap(Map<String, dynamic> map) =>
      DeviceCredentials(
        deviceId: map['device_id'],
        secretKey: map['secret'],
      );
}

class DeviceStorage {
  static const _deviceCredsKey = 'device_credentials';
  static const _deviceIdKey = 'device_id';

  final FlutterSecureStorage _storage;
  final Uuid _uuid;

  DeviceStorage({FlutterSecureStorage? storage, Uuid? uuid})
      : _storage = storage ?? const FlutterSecureStorage(),
        _uuid = uuid ?? const Uuid();

  Future<DeviceCredentials> getOrCreateCredentials() async {
    final existing = await _storage.read(key: _deviceCredsKey);
    
    if (existing != null) {
      try {
        final Map<String, dynamic> data = json.decode(existing);
        return DeviceCredentials.fromMap(data);
      } catch (_) {
        // Invalid data, create new
      }
    }

    // Generate new credentials
    final deviceId = 'dev_${_uuid.v4().substring(0, 12)}';
    final secretKey = _generateSecretKey();
    
    final creds = DeviceCredentials(
      deviceId: deviceId,
      secretKey: secretKey,
    );
    
    await _storage.write(
      key: _deviceCredsKey,
      value: json.encode(creds.toMap()),
    );
    
    return creds;
  }

  String _generateSecretKey() {
    final bytes = _uuid.v4().codeUnits;
    return sha256.convert(bytes).toString().substring(0, 43);
  }

  Future<void> clearCredentials() async {
    await _storage.delete(key: _deviceCredsKey);
  }
}
```

---

## 4. API Client

### 4.1 Dio Client with Interceptors

```dart
// lib/data/services/api_client.dart

import 'package:dio/dio.dart';
import '../storage/token_storage.dart';
import '../storage/device_storage.dart';
import '../../core/config/app_config.dart';

class ApiClient {
  late final Dio _dio;
  final TokenStorage _tokenStorage;
  final DeviceStorage _deviceStorage;

  ApiClient({
    required TokenStorage tokenStorage,
    required DeviceStorage deviceStorage,
  })  : _tokenStorage = tokenStorage,
        _deviceStorage = deviceStorage {
    _dio = Dio(
      BaseOptions(
        baseUrl: AppConfig.apiUrl,
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 60),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    _dio.interceptors.addAll([
      _AuthInterceptor(tokenStorage, deviceStorage, _dio),
      _LoggingInterceptor(),
    ]);
  }

  Dio get dio => _dio;
}

class _AuthInterceptor extends Interceptor {
  final TokenStorage _tokenStorage;
  final DeviceStorage _deviceStorage;
  final Dio _dio;

  _AuthInterceptor(this._tokenStorage, this._deviceStorage, this._dio);

  @override
  void onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    // Skip auth for login endpoints
    if (_isAuthEndpoint(options.path)) {
      return handler.next(options);
    }

    final token = await _tokenStorage.getToken();
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }

    return handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode == 401) {
      // Try to refresh token via device login
      final success = await _refreshToken();
      
      if (success) {
        // Retry the original request
        final token = await _tokenStorage.getToken();
        err.requestOptions.headers['Authorization'] = 'Bearer $token';
        
        try {
          final response = await _dio.fetch(err.requestOptions);
          return handler.resolve(response);
        } catch (e) {
          return handler.next(err);
        }
      }
    }

    return handler.next(err);
  }

  bool _isAuthEndpoint(String path) {
    return path.contains('/auth/device-register') ||
           path.contains('/auth/login') ||
           path.contains('/auth/register');
  }

  Future<bool> _refreshToken() async {
    try {
      final creds = await _deviceStorage.getOrCreateCredentials();
      final response = await _dio.post(
        '/auth/device-register',
        data: {
          'device_id': creds.deviceId,
          'secret_key': creds.secretKey,
        },
      );

      if (response.statusCode == 200) {
        final token = response.data['access_token'];
        await _tokenStorage.saveToken(token);
        return true;
      }
    } catch (_) {}

    return false;
  }
}

class _LoggingInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    print('🌐 [${options.method}] ${options.path}');
    return handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    print('❌ [${err.response?.statusCode}] ${err.requestOptions.path}');
    print('   Error: ${err.message}');
    return handler.next(err);
  }
}
```

### 4.2 Upload Service

```dart
// lib/data/services/upload_service.dart

import 'dart:io';
import 'package:dio/dio.dart';
import 'api_client.dart';

enum UploadCategory {
  condition('condition'),
  solution('solution'),
  epiphany('epiphany'),
  question('question'),
  hint('hint');

  final String value;
  const UploadCategory(this.value);
}

class UploadService {
  final ApiClient _apiClient;

  UploadService({required ApiClient apiClient}) : _apiClient = apiClient;

  Future<bool> uploadImage({
    required UploadCategory category,
    required int entityId,
    required String filePath,
    ProgressCallback? onProgress,
  }) async {
    try {
      final file = File(filePath);
      final fileName = filePath.split('/').last;
      
      final formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(
          filePath,
          filename: fileName,
        ),
      });

      final response = await _apiClient.dio.post(
        '/uploads/${category.value}/$entityId',
        data: formData,
        onSendProgress: onProgress,
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Upload error: $e');
      return false;
    }
  }

  Future<bool> uploadImageBytes({
    required UploadCategory category,
    required int entityId,
    required List<int> bytes,
    required String fileName,
    ProgressCallback? onProgress,
  }) async {
    try {
      final formData = FormData.fromMap({
        'file': MultipartFile.fromBytes(
          bytes,
          filename: fileName,
        ),
      });

      final response = await _apiClient.dio.post(
        '/uploads/${category.value}/$entityId',
        data: formData,
        onSendProgress: onProgress,
      );

      return response.statusCode == 200;
    } catch (e) {
      print('Upload error: $e');
      return false;
    }
  }
}
```

---

## 5. Repositories

### 5.1 Auth Repository

```dart
// lib/data/repositories/auth_repository.dart

import '../models/user.dart';
import '../services/api_client.dart';
import '../storage/token_storage.dart';
import '../storage/device_storage.dart';

class AuthRepository {
  final ApiClient _apiClient;
  final TokenStorage _tokenStorage;
  final DeviceStorage _deviceStorage;

  AuthRepository({
    required ApiClient apiClient,
    required TokenStorage tokenStorage,
    required DeviceStorage deviceStorage,
  })  : _apiClient = apiClient,
        _tokenStorage = tokenStorage,
        _deviceStorage = deviceStorage;

  Future<AuthResponse> deviceLogin() async {
    final creds = await _deviceStorage.getOrCreateCredentials();
    
    final response = await _apiClient.dio.post(
      '/auth/device-register',
      data: {
        'device_id': creds.deviceId,
        'secret_key': creds.secretKey,
      },
    );

    final authResponse = AuthResponse.fromJson(response.data);
    await _tokenStorage.saveToken(authResponse.accessToken);
    
    return authResponse;
  }

  Future<AuthResponse> login({
    required String email,
    required String password,
  }) async {
    final response = await _apiClient.dio.post(
      '/auth/login',
      data: {
        'email': email,
        'password': password,
      },
    );

    final authResponse = AuthResponse.fromJson(response.data);
    await _tokenStorage.saveToken(authResponse.accessToken);
    
    return authResponse;
  }

  Future<UserModel> getMe() async {
    final response = await _apiClient.dio.get('/users/me');
    return UserModel.fromJson(response.data);
  }

  Future<UserModel> convertAccount({
    required String email,
    required String password,
    required String username,
  }) async {
    final response = await _apiClient.dio.patch(
      '/users/me/convert',
      data: {
        'email': email,
        'password': password,
        'username': username,
      },
    );
    
    return UserModel.fromJson(response.data);
  }

  Future<void> logout() async {
    await _tokenStorage.deleteToken();
  }

  Future<bool> isAuthenticated() async {
    return await _tokenStorage.hasToken();
  }
}
```

### 5.2 Problems Repository

```dart
// lib/data/repositories/problems_repository.dart

import '../models/problem.dart';
import '../models/tag.dart';
import '../services/api_client.dart';

class ProblemsRepository {
  final ApiClient _apiClient;

  ProblemsRepository({required ApiClient apiClient}) : _apiClient = apiClient;

  Future<List<SourceModel>> getSources() async {
    final response = await _apiClient.dio.get('/sources');
    return (response.data as List)
        .map((json) => SourceModel.fromJson(json))
        .toList();
  }

  Future<List<ProblemModel>> getProblems({
    String? source,
    String? search,
    String? tag,
    String? reference,
  }) async {
    final queryParams = <String, dynamic>{};
    if (source != null) queryParams['source'] = source;
    if (search != null) queryParams['search'] = search;
    if (tag != null) queryParams['tag'] = tag;
    if (reference != null) queryParams['reference'] = reference;

    final response = await _apiClient.dio.get(
      '/problems',
      queryParameters: queryParams,
    );
    
    return (response.data as List)
        .map((json) => ProblemModel.fromJson(json))
        .toList();
  }

  Future<ProblemModel> getProblem(int id) async {
    final response = await _apiClient.dio.get('/problems/$id');
    return ProblemModel.fromJson(response.data);
  }

  Future<ProblemModel> createProblem(ProblemCreate problem) async {
    final response = await _apiClient.dio.post(
      '/problems',
      data: problem.toJson(),
    );
    return ProblemModel.fromJson(response.data);
  }

  Future<ProblemModel> updateProblem(
    int id, {
    String? conditionText,
    String? reference,
    List<String>? tags,
  }) async {
    final data = <String, dynamic>{};
    if (conditionText != null) data['condition_text'] = conditionText;
    if (reference != null) data['reference'] = reference;
    if (tags != null) data['tags'] = tags;

    final response = await _apiClient.dio.patch(
      '/problems/$id',
      data: data,
    );
    return ProblemModel.fromJson(response.data);
  }

  Future<List<TagModel>> getTags({String? search}) async {
    final queryParams = <String, dynamic>{};
    if (search != null) queryParams['search'] = search;

    final response = await _apiClient.dio.get(
      '/tags',
      queryParameters: queryParams,
    );
    
    return (response.data as List)
        .map((json) => TagModel.fromJson(json))
        .toList();
  }
}
```

### 5.3 Solutions Repository

```dart
// lib/data/repositories/solutions_repository.dart

import '../models/solution.dart';
import '../models/session.dart';
import '../services/api_client.dart';

class SolutionsRepository {
  final ApiClient _apiClient;

  SolutionsRepository({required ApiClient apiClient}) : _apiClient = apiClient;

  Future<List<SolutionModel>> getSolutions({
    int? problemId,
    SolutionStatus? status,
  }) async {
    final queryParams = <String, dynamic>{};
    if (problemId != null) queryParams['problem_id'] = problemId;
    if (status != null) queryParams['status'] = status.name;

    final response = await _apiClient.dio.get(
      '/solutions',
      queryParameters: queryParams,
    );
    
    return (response.data as List)
        .map((json) => SolutionModel.fromJson(json))
        .toList();
  }

  Future<List<SolutionModel>> getActiveSolutions() async {
    return await getSolutions(status: SolutionStatus.active);
  }

  Future<SolutionModel> getSolution(int id) async {
    final response = await _apiClient.dio.get('/solutions/$id');
    return SolutionModel.fromJson(response.data);
  }

  Future<SolutionModel> createSolution(int problemId) async {
    final response = await _apiClient.dio.post(
      '/solutions',
      data: {'problem_id': problemId},
    );
    return SolutionModel.fromJson(response.data);
  }

  Future<SolutionModel> finishSolution(
    int id, {
    required String status,
    int? difficulty,
    double? quality,
    String? notes,
  }) async {
    final response = await _apiClient.dio.patch(
      '/solutions/$id',
      data: {
        'status': status,
        'personal_difficulty': difficulty,
        'quality_score': quality,
        'user_notes': notes,
      },
    );
    return SolutionModel.fromJson(response.data);
  }

  Future<SolutionModel> updateSolutionText(int id, String text) async {
    final response = await _apiClient.dio.patch(
      '/solutions/$id',
      data: {'solution_text': text},
    );
    return SolutionModel.fromJson(response.data);
  }

  Future<SessionModel> createSession(SessionCreate session) async {
    final response = await _apiClient.dio.post(
      '/sessions',
      data: session.toJson(),
    );
    return SessionModel.fromJson(response.data);
  }
}
```

### 5.4 Artifacts Repository

```dart
// lib/data/repositories/artifacts_repository.dart

import '../models/epiphany.dart';
import '../models/question.dart';
import '../models/hint.dart';
import '../models/api_response.dart';
import '../services/api_client.dart';
import '../services/upload_service.dart';

class ArtifactsRepository {
  final ApiClient _apiClient;
  final UploadService _uploadService;

  ArtifactsRepository({
    required ApiClient apiClient,
    required UploadService uploadService,
  })  : _apiClient = apiClient,
        _uploadService = uploadService;

  // Epiphanies
  Future<EpiphanyModel> createEpiphany({
    required int solutionId,
    required String description,
    required int magnitude,
  }) async {
    final response = await _apiClient.dio.post(
      '/epiphanies',
      data: {
        'solution_id': solutionId,
        'description': description,
        'magnitude': magnitude,
      },
    );
    return EpiphanyModel.fromJson(response.data);
  }

  Future<bool> uploadEpiphanyImage(int epiphanyId, String filePath) async {
    return await _uploadService.uploadImage(
      category: UploadCategory.epiphany,
      entityId: epiphanyId,
      filePath: filePath,
    );
  }

  // Questions
  Future<List<QuestionModel>> getQuestions(int solutionId) async {
    final response = await _apiClient.dio.get(
      '/questions/by-solution/$solutionId',
    );
    return (response.data as List)
        .map((json) => QuestionModel.fromJson(json))
        .toList();
  }

  Future<QuestionModel> getQuestion(int id) async {
    final response = await _apiClient.dio.get('/questions/$id');
    return QuestionModel.fromJson(response.data);
  }

  Future<QuestionModel> createQuestion({
    required int solutionId,
    required String body,
  }) async {
    final response = await _apiClient.dio.post(
      '/questions',
      data: {
        'solution_id': solutionId,
        'body': body,
      },
    );
    return QuestionModel.fromJson(response.data);
  }

  Future<bool> answerQuestion(int id, String answer) async {
    final response = await _apiClient.dio.patch(
      '/questions/$id',
      data: {'answer': answer},
    );
    return response.statusCode == 200;
  }

  Future<QuestionModel> generateQuestionAnswer(int id, String persona) async {
    final response = await _apiClient.dio.post(
      '/questions/$id/generate',
      queryParameters: {'persona': persona},
    );
    return QuestionModel.fromJson(response.data);
  }

  Future<bool> uploadQuestionImage(int questionId, String filePath) async {
    return await _uploadService.uploadImage(
      category: UploadCategory.question,
      entityId: questionId,
      filePath: filePath,
    );
  }

  // Hints
  Future<HintModel> createHintDraft({
    required int solutionId,
    String? userNotes,
  }) async {
    final response = await _apiClient.dio.post(
      '/hints/draft',
      data: {
        'solution_id': solutionId,
        'user_notes': userNotes,
      },
    );
    return HintModel.fromJson(response.data);
  }

  Future<List<HintModel>> getHints(int solutionId) async {
    final response = await _apiClient.dio.get(
      '/hints/by-solution/$solutionId',
    );
    return (response.data as List)
        .map((json) => HintModel.fromJson(json))
        .toList();
  }

  Future<HintModel> generateHint(int hintId, String persona) async {
    final response = await _apiClient.dio.post(
      '/hints/$hintId/generate',
      queryParameters: {'persona': persona},
    );
    return HintModel.fromJson(response.data);
  }

  Future<bool> updateHint(int hintId, String hintText) async {
    final response = await _apiClient.dio.patch(
      '/hints/$hintId',
      data: {'hint_text': hintText},
    );
    return response.statusCode == 200;
  }

  Future<bool> uploadHintImage(int hintId, String filePath) async {
    return await _uploadService.uploadImage(
      category: UploadCategory.hint,
      entityId: hintId,
      filePath: filePath,
    );
  }

  // OCR
  Future<String> triggerProblemOcr(int problemId, String persona) async {
    final response = await _apiClient.dio.post(
      '/content/process-image/problem/$problemId',
      queryParameters: {'persona': persona},
    );
    return response.data['text'];
  }

  Future<String> triggerSolutionOcr(int solutionId, String persona) async {
    final response = await _apiClient.dio.post(
      '/content/process-image/solution/$solutionId',
      queryParameters: {'persona': persona},
    );
    return response.data['text'];
  }
}
```

### 5.5 Concepts Repository

```dart
// lib/data/repositories/concepts_repository.dart

import '../models/concept.dart';
import '../services/api_client.dart';

class ConceptsRepository {
  final ApiClient _apiClient;

  ConceptsRepository({required ApiClient apiClient}) : _apiClient = apiClient;

  Future<List<ProblemConceptModel>> analyzeProblem(
    int problemId,
    String persona,
  ) async {
    final response = await _apiClient.dio.post(
      '/concepts/analyze/problem/$problemId',
      queryParameters: {'persona': persona},
    );
    
    return (response.data as List)
        .map((json) => ProblemConceptModel.fromJson(json))
        .toList();
  }

  Future<List<SolutionConceptModel>> analyzeSolution(
    int solutionId,
    String persona,
  ) async {
    final response = await _apiClient.dio.post(
      '/concepts/analyze/solution/$solutionId',
      queryParameters: {'persona': persona},
    );
    
    return (response.data as List)
        .map((json) => SolutionConceptModel.fromJson(json))
        .toList();
  }

  Future<List<ConceptModel>> deduplicateConcepts(String persona) async {
    final response = await _apiClient.dio.post(
      '/concepts/deduplicate',
      queryParameters: {'persona': persona},
    );
    
    return (response.data as List)
        .map((json) => ConceptModel.fromJson(json))
        .toList();
  }
}
```

### 5.6 Billing Repository

```dart
// lib/data/repositories/billing_repository.dart

import '../models/billing.dart';
import '../services/api_client.dart';

class BillingRepository {
  final ApiClient _apiClient;

  BillingRepository({required ApiClient apiClient}) : _apiClient = apiClient;

  Future<BillingBalanceModel> getBalance() async {
    final response = await _apiClient.dio.get('/billing/balance');
    return BillingBalanceModel.fromJson(response.data);
  }

  Future<TopUpResponse> createTopUp(double amount) async {
    final response = await _apiClient.dio.post(
      '/billing/top-up',
      queryParameters: {'amount': amount},
    );
    return TopUpResponse.fromJson(response.data);
  }
}
```

### 5.7 Gamification Repository

```dart
// lib/data/repositories/gamification_repository.dart

import '../models/gamification.dart';
import '../services/api_client.dart';

class GamificationRepository {
  final ApiClient _apiClient;

  GamificationRepository({required ApiClient apiClient}) : _apiClient = apiClient;

  Future<GamificationModel> getMe() async {
    final response = await _apiClient.dio.get('/gamification/me');
    return GamificationModel.fromJson(response.data);
  }

  Future<ActivityResponse> getDailyActivity({int days = 7}) async {
    final response = await _apiClient.dio.get(
      '/gamification/activity/daily',
      queryParameters: {'last_days': days},
    );
    return ActivityResponse.fromJson(response.data);
  }
}
```

---

## 6. DI / Provider Setup

```dart
// lib/core/di/providers.dart

import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/services/api_client.dart';
import '../data/services/upload_service.dart';
import '../data/storage/token_storage.dart';
import '../data/storage/device_storage.dart';
import '../data/repositories/auth_repository.dart';
import '../data/repositories/problems_repository.dart';
import '../data/repositories/solutions_repository.dart';
import '../data/repositories/artifacts_repository.dart';
import '../data/repositories/concepts_repository.dart';
import '../data/repositories/billing_repository.dart';
import '../data/repositories/gamification_repository.dart';

// Storage
final tokenStorageProvider = Provider<TokenStorage>((ref) {
  return TokenStorage();
});

final deviceStorageProvider = Provider<DeviceStorage>((ref) {
  return DeviceStorage();
});

// API Client
final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient(
    tokenStorage: ref.watch(tokenStorageProvider),
    deviceStorage: ref.watch(deviceStorageProvider),
  );
});

final uploadServiceProvider = Provider<UploadService>((ref) {
  return UploadService(apiClient: ref.watch(apiClientProvider));
});

// Repositories
final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepository(
    apiClient: ref.watch(apiClientProvider),
    tokenStorage: ref.watch(tokenStorageProvider),
    deviceStorage: ref.watch(deviceStorageProvider),
  );
});

final problemsRepositoryProvider = Provider<ProblemsRepository>((ref) {
  return ProblemsRepository(apiClient: ref.watch(apiClientProvider));
});

final solutionsRepositoryProvider = Provider<SolutionsRepository>((ref) {
  return SolutionsRepository(apiClient: ref.watch(apiClientProvider));
});

final artifactsRepositoryProvider = Provider<ArtifactsRepository>((ref) {
  return ArtifactsRepository(
    apiClient: ref.watch(apiClientProvider),
    uploadService: ref.watch(uploadServiceProvider),
  );
});

final conceptsRepositoryProvider = Provider<ConceptsRepository>((ref) {
  return ConceptsRepository(apiClient: ref.watch(apiClientProvider));
});

final billingRepositoryProvider = Provider<BillingRepository>((ref) {
  return BillingRepository(apiClient: ref.watch(apiClientProvider));
});

final gamificationRepositoryProvider = Provider<GamificationRepository>((ref) {
  return GamificationRepository(apiClient: ref.watch(apiClientProvider));
});
```

---

*Спецификация API слоя для Flutter приложения "Лежандр"*
