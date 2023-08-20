class PointStyle {
    constructor(base_style) {
        this.show = base_style.show;
        this.pixelSize = base_style.pixelSize;
        this.heightReference = base_style.heightReference;
        this.color = Cesium.Color.fromCssColorString(base_style.color);
        this.outlineColor = Cesium.Color.fromCssColorString(base_style.outlineColor);
        this.outlineWidth = base_style.outlineWidth;
        this.scaleByDistance = new Cesium.NearFarScalar(
            base_style.scaleByDistance.near, base_style.scaleByDistance.nearValue,
            base_style.scaleByDistance.far, base_style.scaleByDistance.farValue
        );
        this.translucencyByDistance = new Cesium.NearFarScalar(
            base_style.translucencyByDistance.near, base_style.translucencyByDistance.nearValue,
            base_style.translucencyByDistance.far, base_style.translucencyByDistance.farValue
        );
        this.distanceDisplayCondition = new Cesium.DistanceDisplayCondition(
            base_style.distanceDisplayCondition.near,
            base_style.distanceDisplayCondition.far
        );
    }
}

class PolylineStyle {
    constructor(base_style) {
        this.show = base_style.show;
        this.width = base_style.width;
        this.clampToGround = base_style.clampToGround;
        this.shadows = base_style.shadows;
        this.zIndex = base_style.clampToGround === true ? base_style.zIndex : undefined;
        this.distanceDisplayCondition = new Cesium.DistanceDisplayCondition(
            base_style.distanceDisplayCondition.near,
            base_style.distanceDisplayCondition.far
        );

        if (base_style.material.type === 'PolylineDash') {
            this.material = new Cesium.PolylineDashMaterialProperty({
                color: Cesium.Color.fromCssColorString(base_style.material.color),
                gapColor: Cesium.Color.fromCssColorString(base_style.material.gapColor),
                dashLength: base_style.material.dashLength
            });
        } else {
            this.material = Cesium.Color.fromCssColorString(base_style.material.color);
        }

        if (base_style.depthFailMaterial) {
            if (base_style.depthFailMaterial.type === 'PolylineDash') {
                this.depthFailMaterial = new Cesium.PolylineDashMaterialProperty({
                    color: Cesium.Color.fromCssColorString(base_style.depthFailMaterial.color),
                    gapColor: Cesium.Color.fromCssColorString(base_style.depthFailMaterial.gapColor),
                    dashLength: base_style.depthFailMaterial.dashLength
                });
            } else {
                this.depthFailMaterial = Cesium.Color.fromCssColorString(base_style.depthFailMaterial.color);
            }
        } else {
            this.depthFailMaterial = this.material
        }
    }
}

class PolygonStyle {
    constructor(base_style) {
        this.show = base_style.show;
        if (base_style.height) {
            this.height = base_style.height;
        }
        this.heightReference = base_style.heightReference;
        if (base_style.extrudedHeight) {
            this.extrudedHeight = base_style.extrudedHeight;
        }
        this.extrudedHeightReference = base_style.extrudedHeightReference;
        this.stRotation = base_style.stRotation;
        this.fill = base_style.fill;
        this.material = Cesium.Color.fromCssColorString(base_style.material.color);
        this.outline = base_style.outline;
        this.outlineColor = Cesium.Color.fromCssColorString(base_style.outlineColor);
        this.outlineWidth = base_style.outlineWidth;
        this.closeTop = base_style.closeTop;
        this.closeBottom = base_style.closeBottom;
        this.shadows = base_style.shadows;
        this.distanceDisplayCondition = new Cesium.DistanceDisplayCondition(
            base_style.distanceDisplayCondition.near,
            base_style.distanceDisplayCondition.far
        );
        this.zIndex = base_style.height === undefined ? base_style.zIndex : undefined;
    }
}

class BillboardStyle {
    constructor(base_style) {
        this.show = base_style.show;
        this.image = base_style.image;
        this.scale = base_style.scale;
        this.pixelOffset = new Cesium.Cartesian2(base_style.pixelOffset.x, base_style.pixelOffset.y);
        this.eyeOffset = new Cesium.Cartesian3(base_style.eyeOffset.x, base_style.eyeOffset.y, base_style.eyeOffset.z);
        this.horizontalOrigin = base_style.horizontalOrigin;
        this.verticalOrigin = base_style.verticalOrigin;
        this.heightReference = base_style.heightReference;
        this.color = Cesium.Color.fromCssColorString(base_style.color);
        this.rotation = base_style.rotation;
        this.alignedAxis = base_style.alignedAxis;
        this.width = base_style.width;
        this.height = base_style.height;
        this.scaleByDistance = new Cesium.NearFarScalar(
            base_style.scaleByDistance.near, base_style.scaleByDistance.nearValue,
            base_style.scaleByDistance.far, base_style.scaleByDistance.farValue
        );
        this.translucencyByDistance = new Cesium.NearFarScalar(
            base_style.translucencyByDistance.near, base_style.translucencyByDistance.nearValue,
            base_style.translucencyByDistance.far, base_style.translucencyByDistance.farValue
        );
        this.pixelOffsetScaleByDistance = new Cesium.NearFarScalar(
            base_style.pixelOffsetScaleByDistance.near, base_style.pixelOffsetScaleByDistance.nearValue,
            base_style.pixelOffsetScaleByDistance.far, base_style.pixelOffsetScaleByDistance.farValue
        );
        this.distanceDisplayCondition = new Cesium.DistanceDisplayCondition(
            base_style.distanceDisplayCondition.near, base_style.distanceDisplayCondition.far
        );
    }
}

class LabelStyle {
    constructor(base_style) {
        this.show = base_style.show;
        this.text = base_style.text;
        this.font = base_style.font;
        this.style = base_style.style;
        this.scale = base_style.scale;
        this.showBackground = base_style.showBackground;
        this.backgroundColor = Cesium.Color.fromCssColorString(base_style.backgroundColor);
        this.backgroundPadding = new Cesium.Cartesian2(base_style.backgroundPadding.x, base_style.backgroundPadding.y);
        this.pixelOffset = new Cesium.Cartesian2(base_style.pixelOffset.x, base_style.pixelOffset.y);
        this.eyeOffset = new Cesium.Cartesian3(base_style.eyeOffset.x, base_style.eyeOffset.y, base_style.eyeOffset.z);
        this.horizontalOrigin = base_style.horizontalOrigin;
        this.verticalOrigin = base_style.verticalOrigin;
        this.heightReference = base_style.heightReference;
        this.fillColor = Cesium.Color.fromCssColorString(base_style.fillColor);
        this.outlineColor = Cesium.Color.fromCssColorString(base_style.outlineColor);
        this.outlineWidth = base_style.outlineWidth;
        this.translucencyByDistance = new Cesium.NearFarScalar(
            base_style.translucencyByDistance.near, base_style.translucencyByDistance.nearValue,
            base_style.translucencyByDistance.far, base_style.translucencyByDistance.farValue
        );
        this.pixelOffsetScaleByDistance = new Cesium.NearFarScalar(
            base_style.pixelOffsetScaleByDistance.near, base_style.pixelOffsetScaleByDistance.nearValue,
            base_style.pixelOffsetScaleByDistance.far, base_style.pixelOffsetScaleByDistance.farValue
        );
        this.scaleByDistance = new Cesium.NearFarScalar(
            base_style.scaleByDistance.near, base_style.scaleByDistance.nearValue,
            base_style.scaleByDistance.far, base_style.scaleByDistance.farValue
        );
        this.distanceDisplayCondition = new Cesium.DistanceDisplayCondition(
            base_style.distanceDisplayCondition.near, base_style.distanceDisplayCondition.far
        );
    }
}

class StyleFactory {
    static createPointStyle(base_style) {
        return new PointStyle(base_style);
    }

    static createPolylineStyle(base_style) {
        return new PolylineStyle(base_style);
    }

    static createPolygonStyle(base_style) {
        return new PolygonStyle(base_style);
    }

    static createBillboardStyle(base_style) {
        return new BillboardStyle(base_style);
    }

    static createLabelStyle(base_style) {
        return new LabelStyle(base_style)
    }
}

const styleTypeMap = {
    Point: StyleFactory.createPointStyle,
    Polyline: StyleFactory.createPolylineStyle,
    Polygon: StyleFactory.createPolygonStyle,
    Billboard: StyleFactory.createBillboardStyle,
    Label: StyleFactory.createLabelStyle
};

async function fetchStyle(type, styleId = null) {
    try {
        const response = await fetch(`/api/${type.toLowerCase()}_styles/` + (styleId ? styleId : ''));
        const data = await response.json();

        const base_style = styleId ? data : data.find(style => style.is_default);
        if (base_style) {
            const styleFactory = styleTypeMap[type];
            if (styleFactory) {
                return styleFactory(base_style);
            } else {
                console.error('Неизвестный тип стиля. Типы: Point, Polyline, Polygon, Billboard, Label');
            }
        } else {
            console.error('Отсутствует базовый стиль для типа ' + type);
            return new Cesium[type + 'Graphics']();
        }
    } catch (error) {
        console.error("Ошибка отправки запроса", error);
    }
}