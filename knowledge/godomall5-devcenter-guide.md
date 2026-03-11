# 고도몰5 개발센터 튜닝 가이드 - 종합 분석

> 출처: https://devcenter-help.nhn-commerce.com
> 분석일: 2026-02-28

---

## 1. 개요

고도몰 튜닝 가이드는 3개 파트로 구성됩니다:
1. **이해하기** - 용어, 구조, 규칙 등 기초
2. **준비하기** - 튜닝 전 사전 준비 (심화 구조, 오픈 API)
3. **튜닝하기** - 실제 튜닝 진행 (소스코드, DB, 디버깅, 패치)

**핵심 경고**: "잘못된 튜닝은 쇼핑몰 운영에 큰 문제가 발생할 수 있습니다"
**책임**: "개발 가이드를 준수하지 않아 발생하는 모든 문제는 전적으로 이용자에게 책임이 있습니다"

---

## 2. 용어 정의

### 튜닝(Tuning)
- 허용된 범위 내에서 고도몰의 기능을 직접 개발하는 것
- 고도몰에서 제공하지 않는 기능을 자체 개발하거나 에이전시를 통해 구현
- 모든 범위가 서로 연계되어 있으므로 가이드 준수 필수

### 패치(Patch)
- 고도몰 솔루션의 업데이트

| 유형 | 설명 | 자동 적용 |
|------|------|----------|
| 프로그램 패치 | 기능(프로그램) 업데이트 | O |
| DB 패치 | 테이블/컬럼 추가·삭제·변경, 데이터 보정 | O |
| 스킨 패치 | 사용자 화면 영역 업데이트 | X (수동) |

### 리드미(ReadMe)
- 스킨 패치 시 제공되는 수동 적용 가이드
- 고도몰 무료 스킨(스토리지, 모먼트 등) 기준으로 패치 내용 설명
- 고객지원 > 소식 > 업데이트 섹션에서 확인

---

## 3. 고도몰 아키텍처

### 3.1 요청 처리 흐름 (5단계)

```
사용자 요청 → Route → Application → Controller → Template → Response
```

1. **Route**: 사용자 요청은 route.php로 전달되어 처리 준비
2. **Application**: 리소스 준비, 적절한 컨트롤러 탐색
3. **Controller**: 요청 처리, 템플릿에 데이터 전달
4. **Template**: Controller로부터 데이터를 받아 HTML 스트링 반환
5. **Response**: 처리된 HTML을 화면에 출력

### 3.2 Route 시스템

- **route.php**: 모든 사용자 요청은 사용자 소스 디렉토리 내 route.php에서 수신 후 처리
- **autoload.php**: ClassLoader를 통해 기본/사용자 소스 디렉토리의 클래스 로드
- **bootstrap.php**: Application 객체 생성 후 필요한 리소스 초기화

#### Rewrite Module 설정
- 모든 Request가 route.php로 전달됨 (정적 리소스 제외)
- 제외 확장자: gif, jpg, jpeg, png, js, css, swf, ico, eot, woff, ttf
- `.htaccess` 규칙으로 제어

```apache
DirectoryIndex route.php
RewriteEngine on
# 정적 파일 + blank.php → 직접 제공
# 나머지 모든 요청 → route.php로 재작성
```

#### 디렉토리별 접근 제어
- **data 디렉토리**: 사용자 정의 파일 저장소 (허용)
  - 차단 확장자: php, htm, log, cgi, inc, xml, json, exe, bat, sh 등 실행파일
- **기타 디렉토리**: 웹에서 접근 제한 (Deny from all)

### 3.3 Application 초기화

1. bootstrap.php에서 Application 객체 생성
2. AbstractBootstrap을 상속받은 클래스를 로드하여 객체를 모두 실행
3. 필요한 클래스를 생성하여 Application 컨테이너에 주입
4. 사용자 요청을 처리할 Controller를 탐색하여 실행

### 3.4 Controller 실행 순서 (9단계)

**초기화:**
1. View 템플릿 엔진 설정
2. `setup()` - interceptor 설정 (인증, 레이아웃, 공통변수)
3. `pre()` - 사용자 정의 전처리 로직

**처리:**
4. Interceptor `preHandle()` 실행 (등록 순서대로)
5. `index()` - 메인 비즈니스 로직 실행
6. Interceptor `postHandle()` 실행 (역순)
7. `post()` - 사용자 정의 후처리 로직

**출력:**
8. `fetch()` - view를 HTML로 변환
9. `render()` - 헤더 설정 후 화면 출력

### 3.5 Controller 클래스 상속 계층

```
AbstractController (추상 클래스)
  └── ActionController (중간 계층)
        ├── Controller\Front\Controller (PC 사용자)
        ├── Controller\Mobile\Controller (모바일 사용자)
        ├── Controller\Admin\Controller (관리자)
        └── Controller\Api\Controller (API)

Widget (컨트롤러 개념이나 현 컨트롤러에 종속)
  └── Widget\Front\Widget
```

#### 영역별 컨트롤러 구현 패턴

```php
// PC 사용자
namespace Bundle\Controller\Front\Test;
class MyController extends \Controller\Front\Controller {
    public function index() { }
}

// 모바일
namespace Bundle\Controller\Mobile\Test;
class MyController extends \Controller\Mobile\Controller { }

// 관리자
namespace Bundle\Controller\Admin\Test;
class MyController extends \Controller\Admin\Controller { }

// API
namespace Bundle\Controller\Api\Test;
class MyController extends \Controller\Api\Controller { }

// Widget
namespace Bundle\Widget\Front\Test;
class MyWidget extends \Widget\Front\Widget { }
```

### 3.6 View 엔진

- **Template_ 엔진**: 사용자 스킨 처리 (Front/Mobile)
- **Include 엔진**: 관리자 스킨 처리 (Admin)

### 3.7 ClassLoader 시스템

- FQN(Fully Qualified Name)을 이용한 autoload 시스템
- 네임스페이스와 물리적 디렉토리 경로가 반드시 동일해야 함

**검색 순서:**
1. 사용자 소스 디렉토리(module)에서 class 검색
2. 없으면 원본 소스 디렉토리(Bundle)에서 검색
3. 사용자 소스에서 발견되면 원본 소스의 class는 무시

---

## 4. 튜닝 가능 범위

### 수정 가능 영역

| 영역 | 설명 |
|------|------|
| `module/Controller` | 사용자 URI 요청에 1:1 대응하는 컨트롤러 |
| `module/Controller/API` | URL 요청에 1:1 대응하는 API 영역 |
| `module/Component` | 비즈니스 로직과 데이터 처리 |
| `module/Widget` | 화면 추가 기능 |
| `module/Asset/Admin` | 관리자 스킨소스 및 메뉴/페이지 |

### 필수 준수사항
- 원본 소스의 class를 **반드시 상속**받을 것
- 메소드 확장 시 **부모 메서드 호출** (parent::method())
- 다른 클래스 사용 시 **namespace와 use 구문** 활용
- module 폴더 외 개발은 운영정책상 **삭제 대상**

### 관리자 스킨소스 특수성
- 상속 개념의 영역이 아님
- 자동패치 미지원
- 패치 적용 시 원본소스를 수동으로 반영

---

## 5. 튜닝 진행 방법

### 3단계 프로세스

1. **원본소스 확인**: 상점 관리자의 '개발소스 관리'에서 접근
2. **소스튜닝**: 원본소스를 기반으로 개발 (로컬 환경)
3. **운영환경 적용**: 튜닝된 소스를 실제 쇼핑몰에 배포

### 자동패치 지원 필수사항
- 원본 소스의 class를 상속받을 것
- 메소드 확장 시 부모 메서드 상속
- 다른 클래스 사용 시 namespace와 use 구문 활용

### 디렉토리 구조 규칙
- 최상위 경로에서 동작하는 파일: `route.php`, `blank.php`만 해당
- 신규 파일 생성: `data`, `skin` 이용
- `tmp`에서 이미지/신규파일 작업 지양 (파일 소실 우려)
- `data`, `skin` 디렉토리: `0707` 이상 권한 필요

---

## 6. 코딩 규칙

### PHP 태그
- `<?php`와 `<?=` 만 사용
- Template 용도: `<?=` 권장
- PHP만 포함된 파일: `?>` 생략

### 들여쓰기
- **4칸 스페이스** (TAB 금지)
- namespace와 PHP 열기 태그는 들여쓰기하지 않음

### 제어 구조
- Alternative syntax 사용 금지
- Control Keyword와 조건문 사이에 반드시 1개 SPACE
- `else if` 대신 `elseif` 사용
- 중괄호 같은 줄에 작성

### 금지 함수

| 금지 함수 | 대체 |
|---------|------|
| `sizeof` | `count` |
| `delete` | `unset` |
| `print` | `echo` |
| `is_null()` | `$var === null` |
| `create_function()` | 익명 함수 |

### 클래스 정의
- 파일당 클래스 1개만
- 클래스명과 파일명 일치 필수
- 중괄호: `{`를 새 줄에 배치
- namespace로 sub-directory 경로 표현

### 연산자 및 기타
- 모든 연산자 앞뒤 스페이스 1개
- Ternary Operator: 중첩 금지, 중간 구문 생략 금지
- Error Control Operators(@) 금지
- 문자열: `'` 기본 사용 (`"` 금지, SQL문 예외)
- Heredoc syntax 금지
- 배열 여러 줄 정의 시 마지막 원소 끝에 `,` 추가
- BOM 없는 UTF-8 인코딩
- 줄바꿈: Unix LF만 사용

### 주석
- Inline: `//` 만 사용 (`#` 금지)
- 2줄 이상의 inline comment 금지
- phpDocumentor 형식 필수
- Task Tags: `@todo` 만 사용 (TODO, FIXME, XXX 금지)

---

## 7. 네이밍 규칙

### 식별자별 스타일

| 대상 | 형식 | 예시 |
|------|------|------|
| 변수 | lowerCamelCase | $fooBar |
| 클래스 | UpperCamelCase | FooBar |
| 네임스페이스 | UpperCamelCase | FooBar |
| 속성 | lowerCamelCase | $fooBar |
| 메서드 | lowerCamelCase | fooBar |
| 상수 | UPPER_CASE_WITH_UNDERSCORES | FOO_BAR |
| 내부함수 | lower_case_with_underscore + `gd_` prefix | gd_mysql_query |
| DB 테이블 | lower_case_with_underscores + prefix | es_goods |
| DB 컬럼 | lower_case_with_underscores | goods_name |
| DB 인덱스 | uidx (Unique) / idx (Index) + 컬럼명 | uidx_goods_name |

### 클래스/인터페이스 접미사/접두사
- Interface: 접미사 "Interface"
- Trait: 접미사 "Trait"
- 추상클래스: 접두사 "Abstract"
- 예외클래스: 접두사 "Exception"

### 메서드
- 동사로 시작
- Visibility 반드시 지정
- private 메서드만 언더스코어(_) 시작

### DB 규칙
- Triggers, Stored Procedures, UDF, Views: **사용 금지**

---

## 8. 심화 구조 - HTTP

### Request
- `$_GET`, `$_POST`, `$_FILES`, `$_SERVER`, `$_REQUEST` 지원 (`$_ENV` 미지원)
- 점 표기법(dot notation)으로 다차원 키 접근 가능
- 메서드 체이닝: `Request::get()`, `Request::post()`, `Request::server()`, `Request::files()`, `Request::request()`

**CRUD:**
- 조회: `get('key', '기본값')`, `all()`, `toArray()`
- 설정: `set('name', 'value')`
- 삭제: `del('key')`, `clear()`
- 확인: `has('key')`

**주요 메서드:**

| 메서드 | 기능 |
|--------|------|
| `getServerAddress()` | 서버 IP |
| `getRemoteAddress()` | 클라이언트 IP (Proxy/nginx 대응) |
| `isCli()` | CLI 접근 여부 |
| `isAjax()` | AJAX 요청 확인 |
| `isMethod($method)` | HTTP 메서드 검증 |
| `isMobile()` | 도메인 'm' 포함 여부 |
| `isMobileDevice()` | UserAgent 기반 기기 타입 |
| `isRefresh()` | 브라우저 새로고침 감지 |

### Response
- Json, Redirect, Streamed, BinaryFile 4가지 형태

### Session
- 파일 기반만 지원
- 점 표기법 지원
- `set()`, `get()`, `all()`, `del()`, `clear()`, `has()`

### Cookie
- 다차원 키 미지원
- `set('name', 'value', 3600, '/', true, true')` - 만료시간, 경로, secure, httponly

---

## 9. 심화 구조 - 데이터베이스 메서드

### DB 로드
```php
$this->db = \App::load('DB');
```

### 핵심 메서드

| 메서드 | 기능 |
|--------|------|
| `bind_param_push()` | 바인딩 파라미터 저장 |
| `query_complete()` | 쿼리 조각(field, join, where, group, order, limit) 조합 |
| `query_fetch()` | 쿼리 실행 및 결과 반환 |
| `get_binding()` | 필드 추출/제외하여 바인딩 데이터 반환 |
| `set_insert_db()` | INSERT 실행 |
| `set_update_db()` | UPDATE 실행 (영향 레코드 수 반환) |
| `set_delete_db()` | DELETE 실행 (영향 레코드 수 반환) |
| `bind_query()` | SQL + 바인딩 파라미터 직접 실행 |
| `getCount()` | 조회 결과 행 개수 반환 |

### 트랜잭션
```php
$this->db->begin_tran();
$this->db->commit();
$this->db->rollback();
// 또는
$this->db->transaction(function() { ... });
```

### Master/Slave DB 분리
```php
// Master DB
$this->db->query_fetch($query);

// Slave DB (읽기 전용)
$this->db->slave()->query_fetch($query);
// Slave 없을 시 자동으로 Master로 전환
```

활용 대상: 페이징 count 쿼리, 실시간 업데이트 불필요 쿼리, 설정 저장 쿼리

---

## 10. 심화 구조 - 보안

### Encryptor (암호화)
- 대칭 키 암호화: RIJNDAEL 256 알고리즘
- 패스워드 관리: BCRYPT HASH

```php
// 암호화
Encryptor::encrypt('value');
Encryptor::encrypt('value', 'salt string');

// 복호화
Encryptor::decrypt($encrypted);
```

- MySQL AES 호환 (DB 연결 없이 독립적 암호화 가능)

### Password
```php
Password::hash('password');          // 해싱
Password::verify('password', $hash); // 검증
Password::needsRehash($hash);       // 재해싱 필요 여부
```

---

## 11. 심화 구조 - 예외 처리

| Exception 클래스 | 동작 |
|------------------|------|
| `AlertBackException` | 경고창 후 이전 페이지 이동 |
| `AlertCloseException` | 경고 후 브라우저 탭/창 종료 |
| `LayerException` | 레이어 팝업에 메시지 출력 |
| `AlertOnlyException` | 경고창에 메시지만 출력 |
| `AlertRedirectException` | 경고창 후 지정 URL 이동 |
| `HttpException` | HTTP 상태 코드 + 에러 페이지 렌더링 |
| `DatabaseException` | DB 쿼리 실행 오류 (`$e->getQuery()` 가능) |
| `UploadException` | 파일 업로드 오류 |

```php
// 사용 예시
throw new AlertBackException('오류 메시지');
throw new AlertRedirectException('메시지', null, null, $url, $target);
throw new HttpException($message, 404);
throw new DatabaseException($message, $code, $previous, $query);
```

---

## 12. 심화 구조 - 다국어 (Language)

- getText 방식 적용
- 튜닝샵은 별도 언어 설정 미지원

### 번역 함수

| 함수 | 기능 |
|------|------|
| `__()` | 기본 번역 |
| `n__()` | 복수형 처리 |
| `p__()` | 문맥별 구분 |
| `d__()` | 도메인 지정 |
| `dp__()` | 도메인 + 문맥 |
| `dnp__()` | 도메인 + 문맥 + 복수 |

```php
__('오류가 발생하였습니다.');
__('%s 오류가 발생하였습니다.', $errorCode);
n__('테스트', '테스트들', 2);  // 복수형
p__('메뉴', '테스트');          // 문맥 구분
d__('도메인1', '테스트');       // 도메인 지정
```

---

## 13. 데이터베이스 튜닝

### 테이블 생성 규칙
- **Engine**: InnoDB 필수 (다른 타입 사용 시 테이블 손상 위험)
- **Character Set**: utf8mb4
- **Collation**: utf8mb4_general_ci
- **Primary Key**: InnoDB 기반 정렬/저장에 필수
- **Comment**: 테이블과 컬럼의 용도 명시 필수
- **Prefix**: 고유 접두사 사용 (es_, zz_ 제외)
- 솔루션 기본 제공 테이블/컬럼 수정/삭제 **절대 금지**

### 컬럼 생성 규칙
- NotNull 컬럼은 기본값 필수
- Comment 필수
- 솔루션 기본 Data Type 수정 금지

### 쿼리 최적화 원칙

1. **데이터 타입 일치**
```sql
-- 올바름
WHERE orderNo = '123456'    -- 문자형
WHERE goodsNo = 123456      -- 숫자형
```

2. **SELECT 절 최적화**: `*` 자제, 필요한 컬럼만 조회

3. **WHERE 절 필수**: 조건 없으면 전체 테이블 조회 발생

4. **불필요한 연산 제거**: 미참조 JOIN 금지, 집계함수 없는 GROUP BY 금지

5. **인덱스 활용**
```sql
-- 비효율 (인덱스 미사용)
WHERE SUBSTR(orderStatus, 1, 1) = 'o'

-- 효율적 (인덱스 사용)
WHERE orderStatus LIKE 'o%'
```

### DBTableField 확장

**테이블 추가:**
```php
namespace Component\Database;
class DBTableField extends \Bundle\Component\Database\DBTableField
{
    public static function tableTestTable()
    {
        $arrField = [
            ['val' => 'sno', 'typ' => 'i', 'def' => null],
            ['val' => 'testNo', 'typ' => 'i', 'def' => '1'],
        ];
        return $arrField;
    }
}
```

**기존 테이블에 컬럼 추가:**
```php
public static function tableGoods($conf = null)
{
    $arrField = parent::tableGoods($conf);
    $arrField[] = ['val' => 'testNo', 'typ' => 'i', 'def' => '1'];
    return $arrField;
}
```

- 메서드명: `table` + 테이블명(es_ 제외, 첫글자 대문자)
- 필드 정의: val(컬럼명), typ(i=숫자/s=문자), def(기본값)

### DB 튜닝 유의사항
- 작업 전 **테이블 백업 필수** (phpMyAdmin export 사용)
- CTAS 방식 지양 (Lock 발생, 서버 부하)
- MySQL **예약어 사용 금지** (rank, order 등)
- **특수문자 사용 금지** (허용: 0-9, a-z, A-Z, $, _)
- 접두사 미사용, 테이블/컬럼 수정·삭제로 인한 오류는 사용자 책임

### PhpMyAdmin
- 직접 설치 금지 (2021.09.01~, 보안 사유)
- 고도몰 pro / business(pro+)에서만 제공
- IP 등록 → 비밀번호 확인 → DB 인증 → 데이터 관리

---

## 14. Controller 데이터 핸들링

### setData / getData 패턴

**Controller → View 데이터 전달:**
```php
$this->setData('setData', $value);
```

**관리자 스킨에서 사용 (PHP):**
```php
<?=$setData;?>
```

**사용자 스킨에서 사용 (치환코드):**
```html
{=setData}
```

### 조건부 렌더링 (사용자 스킨 문법)
```html
<!--{ ? isset(displayBox) === true }-->
<div>{=displayBox}</div>
<!--{ / }-->
```

### 출력 메서드
- **HTML 렌더링**: 기본 (스킨 파일 자동 매핑)
- **JSON 출력**: `$this->json($data)` 또는 `setData('wrapper', [...])` 후 `json()`
- **파일 다운로드**: `$this->download(경로, 파일명)` / `streamedDownload('파일명')`
- **리다이렉트**: `$this->redirect('../경로')`

---

## 15. 디버깅

### 접근 조건
- 고도몰 **PRO 이상**에서만 사용
- 관리자 계정에 **디버그 권한** 필요
- **로그인 세션이 유효한 상태**에서만 표시

### 디버깅 정보
- **런타임 에러**: 에러명, 에러메시지, 발생 시각, 발생 위치
- **데이터베이스 에러**: 에러명(DatabaseException), 에러메시지, 에러 쿼리, 발생 시각, 발생 위치

---

## 16. 패치 확인 및 대응

### 소스 배포 (자동)
- 배포 공지사항에서 개선되는 Class/Method 정보 확인
- 커스텀 개발 가이드 준수 여부 검토

### 스킨 배포 (수동, 8단계)
1. NHN커머스 사이트 로그인 → 내 쇼핑몰 관리
2. 패치&업그레이드 메뉴 선택
3. 패치 필요한 쇼핑몰 도메인 클릭
4. 적용할 패치 게시글 선택
5. 패치 파일 다운로드
6. 압축 파일 검토 (스킨수정 파일, 패치 내용 파일, data 폴더)
7. 로컬에서 패치 작업 후 '패치확인하기' 클릭
8. 패치 완료 기록

---

## 17. 튜닝 예제

### 17.1 관리자 GNB 색상 변경

**수정 파일:** `admin/css/admin-custom.css`

```css
#header .navbar {
    background-color: #213D54;
}
#header .nav.navbar-nav.reform {
    background-color: #5A86CB;
}
```

### 17.2 관리자 페이지 추가

**컨트롤러 파일:** `module/Controller/Admin/Policy/MenuManagementController.php`

```php
namespace Controller\Admin\Policy;

class MenuManagementController extends \Controller\Admin\Controller
{
    public function index()
    {
        try {
            $this->callMenu('policy', 'menu', 'menu_management');
            $setData = 'Hello World!';
            $this->setData('setData', $setData);
        } catch (\Exception $e) {
            throw $e;
        }
    }
}
```

**스킨 파일:** `admin/policy/menu_management.php`
```php
<?=$setData;?>
```

**액션 처리 방식 (JSON/직접 출력):**
```php
public function index()
{
    try {
        $setData = 'Hello World!';
        echo $setData;
        exit();
    } catch (\Exception $e) {
        throw $e;
    }
}
```

### 17.3 사용자 페이지 추가

**컨트롤러:** `module/Controller/Front/Test/SampleController.php`
```php
namespace Controller\Front\Test;

class SampleController extends \Controller\Front\Controller
{
    public function index()
    {
        $setData = 'Hello World !!!';
        $this->setData('setData', $setData);
    }
}
```

**스킨:** `data/skin/front/[스킨명]/test/sample.html`
```html
<table border="1">
    <tr><td>{=setData}</td></tr>
</table>
```

### 17.4 관리자 페이지 수정 (상속 패턴)

```php
namespace Controller\Admin\Order;

class OrderListAllController extends \Bundle\Controller\Admin\Order\OrderListAllController
{
    public function index()
    {
        try {
            parent::index();  // 기존 기능 유지
            $this->setData('newData', $newValue);
        } catch (\Exception $e) {
            throw $e;
        }
    }
}
```

### 17.5 사용자 페이지 수정 (상속 패턴)

```php
namespace Controller\Front\Order;

class CartController extends \Bundle\Controller\Front\Order\CartController
{
    public function index()
    {
        try {
            parent::index();  // 기존 기능 유지
            $displayBox = '박스를 출력';
            $this->setData('displayBox', $displayBox);
        } catch (\Exception $e) {
            throw $e;
        }
    }
}
```

스킨에서 조건부 출력:
```html
<!--{ ? isset(displayBox) === true }-->
<div style="margin-top:10px; padding:10px; text-align:center; border:3px solid #cfcfcf;">
    {=displayBox}
</div>
<!--{ / }-->
```

### 17.6 관리자 메뉴 추가

**메뉴 테이블:** `es_adminMenu`

**Prefix 규칙:** godo 사용 금지 (배포 시 초기화), 자체 prefix 사용

**1차 메뉴 추가:**
```sql
INSERT INTO `es_adminMenu` (adminMenuNo, adminMenuType, adminMenuProductCode,
  adminMenuPlusCode, adminMenuCode, adminMenuDepth, adminMenuParentNo,
  adminMenuSort, adminMenuName, adminMenuUrl, adminMenuDisplayType,
  adminMenuDisplayNo, adminMenuSettingType, adminMenuEcKind, regDt)
VALUES ('prefix00120', 'd', 'godomall', null, 'setting', '1', 'setting',
  '101', '환경저장', 'setting.php', 'y', 'godo00000', 'd', 'p', now());
```

**2차 메뉴**: 1개 이상의 3차 메뉴가 등록되어야 노출

**권한 설정:**
```php
$writable = $this->getAdminMenuWritableAuth();
if ($writable['check'] === false) {
    // 쓰기 권한 없음 처리
}
```

### 17.7 메뉴 수정

```sql
-- 메뉴명 변경
UPDATE `es_adminMenu` SET adminMenuName = '광고설정' WHERE adminMenuNo = 'prefix00120';

-- URL 변경
UPDATE `es_adminMenu` SET adminMenuUrl = 'advertisement.php' WHERE adminMenuNo = 'prefix00120';

-- 노출 여부 변경
UPDATE `es_adminMenu` SET adminMenuDisplayType = 'n' WHERE adminMenuNo = 'prefix00120';
```

### 17.8 즐겨찾기 메뉴 바로가기

**수정 대상:** `admin/base/index.php` (관리자 메인)
- 개발소스관리에서 원본을 운영소스에 복사 후 수정
- HTML 버튼 + CSS 스타일 추가

---

## 18. 잘못된 튜닝 사례

### 18.1 상속처리 미적용

**잘못된 패턴:**
```php
class ExcelRequest extends \Bundle\Component\Excel\ExcelRequest
{
    public function saveInfoExcelRequest($arrData)
    {
        // 부모 클래스 메서드 호출 없음 - 위험!
    }
}
```

**올바른 패턴:**
```php
class ExcelRequest extends \Bundle\Component\Excel\ExcelRequest
{
    public function saveInfoExcelRequest($arrData)
    {
        parent::saveInfoExcelRequest($arrData); // 부모 호출 필수
        // 추가 로직
    }
}
```

### 18.2 불필요한 메소드 오버라이딩

**잘못된 패턴:** 부모와 동일한 로직만 포함한 오버라이드 메소드

**올바른 대응:** 메소드 자체를 삭제 → 부모 클래스의 최신 구현을 자동 상속

### 18.3 보고된 실전 이슈 6가지

1. **마스터 DB 과부하**: Slave DB 활용하여 읽기 전용 쿼리 분산
2. **분산서버 미고려**: 파일을 원본서버에만 저장하도록 변경
3. **DB 컬럼값 임의 변경**: adminMenuNo 등 고도몰 정의 값 변경 금지, 자체 prefix 사용
4. **튜닝 내용 불완전 적용**: form id 변경 시 관련 파일 모두 일관 반영
5. **이미지 바이너리 DB 저장**: DB에 바이너리 데이터 저장 금지, 파일 경로만 저장 (서버 부하, 상점 차단 가능)
6. **NOT NULL 필드 기본값 미설정**: ALTER TABLE 사용 시 DEFAULT 값 반드시 지정

---

## 19. 오픈 API

### 인증키 구성
- **제휴사 키**: 개발 조직에 발급되는 인증키
- **사용자 키**: 제휴사 키와 쇼핑몰에 매칭되는 고유 인증키

### 발급 절차
1. 개발자 등록 (개발사 일회성 신청)
2. 담당자 승인 후 사용자키 신청 URL 확인
3. 쇼핑몰 선택 (고도 회원 ID + 도메인)
4. 이메일 인증 (유효기간 내)
5. 담당자 검토 후 키값 전달

### 공급사 API
- 기존 오픈API와 동일 방식
- 공급사 계정으로 접근 시 해당 공급사 정보로만 조회/등록/수정/삭제 제한
- 상품 승인 권한과 기능 권한에 따라 추가 제한

---

## 20. 기타 가이드

### PHP 표준 준수
- 고도몰의 PHP 소스는 PHP-FIG(Framework Interop Group)의 표준 권장사항을 따름
- 공식 사이트: https://www.php-fig.org/

---

## 부록: 짱베이스볼 적용 시 주의사항

### 적용 가능한 커스터마이징 범위
1. `module/Controller` - 사용자/관리자 컨트롤러 확장
2. `module/Component` - 비즈니스 로직 확장
3. `module/Widget` - 위젯 추가
4. `module/Asset/Admin` - 관리자 스킨 수정
5. `data/skin/front/` - 사용자 스킨 수정 (치환코드 활용)
6. DB 테이블 추가 (자체 prefix 사용, es_/zz_ 금지)

### 절대 금지 사항
- 고도몰 코어 파일(Bundle/) 직접 수정
- 기본 제공 테이블/컬럼 수정/삭제
- module 폴더 외 PHP 개발
- godo prefix로 메뉴 추가
- 이미지 바이너리를 DB에 저장
- tmp 폴더에 파일 생성

### 개발 프로세스
1. 개발소스관리에서 원본소스 확인
2. 원본 클래스를 상속받아 module/ 내에서 확장
3. parent::method() 호출로 기존 기능 유지
4. 로컬 테스트 후 운영환경 적용
5. 패치 공지사항 확인 → 충돌 여부 검토
