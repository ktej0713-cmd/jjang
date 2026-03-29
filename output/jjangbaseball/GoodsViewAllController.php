<?php
/**
 * 짱베이스볼 커스텀 모듈 — 실행 순서 테스트
 * setData를 parent::index() 앞에서 호출
 *
 * 업로드 경로:
 *   /module/Controller/Front/Goods/GoodsViewAllController.php
 */

namespace Controller\Front\Goods;

class GoodsViewAllController extends \Bundle\Controller\Front\Goods\GoodsViewAllController
{
    public function index()
    {
        // parent 실행 전에 미리 세팅 — 템플릿 렌더가 parent 내부에서 일어날 경우 대비
        try {
            $this->setData('goodsImageUrl', 'TEST_OK');
        } catch (\Exception $e) {}

        parent::index();
    }
}
