document.addEventListener('DOMContentLoaded', () => {
    initCalculations();
    initExport();
    initLoad();
    setCurrentDate();
});

function setCurrentDate() {
    const now = new Date();
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    document.getElementById('currentDate').textContent = now.toLocaleDateString('es-ES', options);
}

function initCalculations() {
    const lotLength = document.getElementById('lotLength');
    const lotWidth = document.getElementById('lotWidth');
    const levels = document.getElementById('levels');
    const floorHeight = document.getElementById('floorHeight');
    const totalArea = document.getElementById('totalArea');
    const budgetTotal = document.getElementById('budgetTotal');

    function updateLotArea() {
        const area = parseFloat(lotLength.value) * parseFloat(lotWidth.value);
        document.getElementById('lotArea').value = area.toFixed(0);
    }

    function updateTotalHeight() {
        const height = parseInt(levels.value) * parseFloat(floorHeight.value);
        document.getElementById('totalHeight').value = height.toFixed(1);
    }

    function updateCostPerM2() {
        const cost = parseFloat(budgetTotal.value) / parseFloat(totalArea.value);
        document.getElementById('costPerM2').value = cost.toFixed(0);
    }

    lotLength.addEventListener('input', updateLotArea);
    lotWidth.addEventListener('input', updateLotArea);
    levels.addEventListener('input', updateTotalHeight);
    floorHeight.addEventListener('input', updateTotalHeight);
    totalArea.addEventListener('input', updateCostPerM2);
    budgetTotal.addEventListener('input', updateCostPerM2);

    updateLotArea();
    updateTotalHeight();
    updateCostPerM2();
}

function initExport() {
    document.getElementById('btn-export-txt').addEventListener('click', exportTXT);
    document.getElementById('btn-export-json').addEventListener('click', exportJSON);
    document.getElementById('btn-save-db').addEventListener('click', saveDT);
}

function initLoad() {
    const fileInput = document.getElementById('fileInput');
    
    document.getElementById('btn-load').addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        const reader = new FileReader();
        reader.onload = (event) => {
            try {
                const data = JSON.parse(event.target.result);
                loadFromJSON(data);
                alert('Proyecto cargado correctamente');
            } catch (err) {
                alert('Error al cargar el archivo: ' + err.message);
            }
        };
        reader.readAsText(file);
    });
}

function collectData() {
    const data = {
        project: {
            name: document.getElementById('projectName').value,
            code: document.getElementById('projectCode').value,
            client: document.getElementById('clientName').value,
            location: document.getElementById('location').value,
            exportDate: new Date().toISOString()
        },
        site: {
            lot: {
                length: parseFloat(document.getElementById('lotLength').value),
                width: parseFloat(document.getElementById('lotWidth').value),
                area: parseFloat(document.getElementById('lotArea').value),
                shape: document.getElementById('lotShape').value,
                dimensions: document.getElementById('lotDimensions').value
            },
            topography: {
                slope: document.getElementById('topography').value,
                direction: document.getElementById('slopeDirection').value,
                elevation: parseFloat(document.getElementById('elevation').value),
                soilType: document.getElementById('soilType').value,
                soilNotes: document.getElementById('soilNotes').value
            },
            climate: {
                type: document.getElementById('climate').value,
                altitudeZone: document.getElementById('altitudeZone').value,
                tempMax: parseFloat(document.getElementById('tempMax').value),
                tempMin: parseFloat(document.getElementById('tempMin').value),
                tempAvg: parseFloat(document.getElementById('tempAvg').value),
                rainfall: parseFloat(document.getElementById('rainfall').value),
                humidity: parseFloat(document.getElementById('humidity').value),
                sunHours: parseFloat(document.getElementById('sunHours').value),
                windDirection: document.getElementById('windDirection').value,
                windSpeed: parseFloat(document.getElementById('windSpeed').value),
                seismicZone: document.getElementById('seismicZone').value,
                riskZone: document.getElementById('riskZone').value
            },
            orientation: {
                main: document.getElementById('orientation').value,
                sunPath: document.getElementById('sunPath').value,
                shadeNorth: document.getElementById('shadeNorth').checked,
                shadeSouth: document.getElementById('shadeSouth').checked,
                shadeEast: document.getElementById('shadeEast').checked,
                shadeWest: document.getElementById('shadeWest').checked,
                shadeTrees: document.getElementById('shadeTrees').checked,
                shadeMountain: document.getElementById('shadeMountain').checked
            },
            surroundings: {
                zoneType: document.getElementById('zoneType').value,
                description: document.getElementById('surroundings').value,
                vegetation: document.getElementById('envVegetation').checked,
                quiet: document.getElementById('envQuiet').checked,
                viewGood: document.getElementById('envViewGood').checked,
                noise: document.getElementById('envNoise').checked,
                pollution: document.getElementById('envPollution').checked,
                security: document.getElementById('envSecurity').checked
            },
            services: {
                water: document.getElementById('svcWater').checked,
                sewer: document.getElementById('svcSewer').checked,
                electric: document.getElementById('svcElectric').checked,
                gas: document.getElementById('svcGas').checked,
                internet: document.getElementById('svcInternet').checked,
                paved: document.getElementById('svcPaved').checked,
                streetLight: document.getElementById('svcStreetLight').checked,
                garbage: document.getElementById('svcGarbage').checked,
                waterSource: document.getElementById('waterSource').value,
                sewageSystem: document.getElementById('sewageSystem').value
            }
        },
        regulations: {
            type: document.getElementById('regulationType').value,
            code: document.getElementById('regulationCode').value,
            zoning: document.getElementById('zoning').value,
            setbacks: {
                front: parseFloat(document.getElementById('setbackFront').value),
                back: parseFloat(document.getElementById('setbackBack').value),
                side: parseFloat(document.getElementById('setbackSide').value),
                notes: document.getElementById('setbackNotes').value
            },
            limits: {
                maxHeight: parseFloat(document.getElementById('maxHeight').value),
                maxLevels: parseInt(document.getElementById('maxLevels').value),
                maxFloorHeight: parseFloat(document.getElementById('maxFloorHeight').value),
                maxCoverage: parseFloat(document.getElementById('maxCoverage').value),
                maxFSI: parseFloat(document.getElementById('maxFSI').value),
                maxGSI: parseFloat(document.getElementById('maxGSI').value)
            },
            parking: {
                required: parseInt(document.getElementById('parking').value),
                bike: parseInt(document.getElementById('bikeParking').value),
                visitors: parseInt(document.getElementById('visitorsParking').value),
                accessType: document.getElementById('accessType').value
            },
            requirements: {
                accessibility: document.getElementById('reqAccessibility').checked,
                fire: document.getElementById('reqFire').checked,
                seismic: document.getElementById('reqSeismic').checked,
                energy: document.getElementById('reqEnergy').checked,
                water: document.getElementById('reqWater').checked,
                green: document.getElementById('reqGreen').checked,
                noise: document.getElementById('reqNoise').checked,
                environmental: document.getElementById('reqEnv').checked,
                historic: document.getElementById('reqHistoric').checked,
                heightLimit: document.getElementById('reqHeightLimit').checked,
                notes: document.getElementById('reqNotes').value
            },
            greenArea: {
                required: parseFloat(document.getElementById('greenAreaReq').value),
                setbackGreen: document.getElementById('setbackGreen').value
            }
        },
        program: {
            general: {
                totalArea: parseFloat(document.getElementById('totalArea').value),
                levels: parseInt(document.getElementById('levels').value),
                floorHeight: parseFloat(document.getElementById('floorHeight').value),
                totalHeight: parseFloat(document.getElementById('totalHeight').value),
                ceilingHeight: parseFloat(document.getElementById('ceilingHeight').value),
                slabThickness: parseFloat(document.getElementById('slabThickness').value)
            },
            level1: {
                area: parseFloat(document.getElementById('level1Area').value),
                use: document.getElementById('level1Use').value,
                program: document.getElementById('level1Program').value,
                notes: document.getElementById('level1Notes').value
            },
            level2: {
                area: parseFloat(document.getElementById('level2Area').value),
                use: document.getElementById('level2Use').value,
                program: document.getElementById('level2Program').value,
                notes: document.getElementById('level2Notes').value
            },
            spaces: {
                terrace: document.getElementById('spTerrace').checked,
                patio: document.getElementById('spPatio').checked,
                garage: document.getElementById('spGarage').checked,
                storage: document.getElementById('spStorage').checked,
                pool: document.getElementById('spPool').checked,
                garden: document.getElementById('spGarden').checked,
                bbq: document.getElementById('spBBQ').checked,
                gym: document.getElementById('spGym').checked,
                office: document.getElementById('spOffice').checked
            },
            wetZones: {
                bathrooms: parseFloat(document.getElementById('bathrooms').value),
                kitchenCount: parseInt(document.getElementById('kitchenCount').value),
                distribution: document.getElementById('wetZones').value
            },
            special: document.getElementById('specialReq').value,
            flexibility: document.getElementById('flexibility').value
        },
        design: {
            concept: {
                style: document.getElementById('designStyle').value,
                philosophy: document.getElementById('designPhilosophy').value,
                description: document.getElementById('designConcept').value
            },
            proportions: {
                system: document.getElementById('proportionSystem').value,
                moduleSize: parseFloat(document.getElementById('moduleSize').value),
                facade: document.getElementById('facadeProportion').value,
                volumetry: document.getElementById('volumetry').value
            },
            roof: {
                type: document.getElementById('roofType').value,
                material: document.getElementById('roofMaterial').value,
                pitch: parseFloat(document.getElementById('roofPitch').value),
                overhang: parseFloat(document.getElementById('roofOverhang').value),
                height: parseFloat(document.getElementById('roofHeight').value)
            },
            windows: {
                width: parseFloat(document.getElementById('windowWidth').value),
                height: parseFloat(document.getElementById('windowHeight').value),
                ratio: parseFloat(document.getElementById('windowRatio').value),
                orientation: document.getElementById('windowOrientation').value,
                type: document.getElementById('windowType').value,
                specials: {
                    floorToCeiling: document.getElementById('winFloorToCeiling').checked,
                    clerestory: document.getElementById('winClerestory').checked,
                    skylight: document.getElementById('winSkylight').checked,
                    corner: document.getElementById('winCorner').checked,
                    bay: document.getElementById('winBay').checked,
                    ribbon: document.getElementById('winRibbon').checked
                }
            },
            doors: {
                main: document.getElementById('mainDoor').value,
                mainHeight: parseFloat(document.getElementById('mainDoorHeight').value),
                interior: document.getElementById('interiorDoors').value
            },
            facade: document.getElementById('facadeTreatment').value
        },
        materials: {
            walls: {
                structural: document.getElementById('wallStructural').value,
                thickness: parseFloat(document.getElementById('wallThickness').value),
                finish: document.getElementById('wallMaterial').value,
                texture: document.getElementById('wallFinish').value
            },
            accent: {
                material: document.getElementById('accentMaterial').value,
                location: document.getElementById('accentLocation').value
            },
            floors: {
                interior: document.getElementById('floorInterior').value,
                exterior: document.getElementById('floorExt').value
            },
            glass: {
                type: document.getElementById('glassType').value,
                thickness: document.getElementById('glassThickness').value
            },
            frames: {
                material: document.getElementById('frameMaterial').value,
                color: document.getElementById('frameColor').value
            },
            notes: document.getElementById('materialNotes').value,
            certifications: {
                fsc: document.getElementById('certFSC').checked,
                recycle: document.getElementById('certRecycle').checked,
                local: document.getElementById('certLocal').checked,
                lowVOC: document.getElementById('certLowVOC').checked,
                energyStar: document.getElementById('certEnergyStar').checked
            }
        },
        sustainability: {
            passive: {
                crossVentilation: document.getElementById('bio_crossVent').checked,
                stackVentilation: document.getElementById('bio_stackVent').checked,
                naturalLight: document.getElementById('bio_naturalLight').checked,
                solarGain: document.getElementById('bio_solarGain').checked,
                thermalMass: document.getElementById('bio_thermalMass').checked,
                shading: document.getElementById('bio_shading').checked,
                evaporative: document.getElementById('bio_evaporative').checked,
                greenRoof: document.getElementById('bio_greenRoof').checked,
                greenFacade: document.getElementById('bio_greenFacade').checked,
                earthTube: document.getElementById('bio_earthTube').checked,
                nightFlush: document.getElementById('bio_nightFlush').checked,
                sunBreakers: document.getElementById('bio_sunBreakers').checked
            },
            active: {
                solarPV: document.getElementById('act_solar').checked,
                solarHeat: document.getElementById('act_solarHeat').checked,
                heatPump: document.getElementById('act_heatPump').checked,
                rainwater: document.getElementById('act_rainwater').checked,
                grayWater: document.getElementById('act_grayWater').checked,
                smartHome: document.getElementById('act_smartHome').checked,
                led: document.getElementById('act_led').checked,
                evCharger: document.getElementById('act_evCharger').checked
            },
            energy: {
                target: document.getElementById('energyTarget').value,
                insulation: document.getElementById('insulationLevel').value,
                uWall: parseFloat(document.getElementById('uWall').value),
                uRoof: parseFloat(document.getElementById('uRoof').value),
                uWindow: parseFloat(document.getElementById('uWindow').value)
            },
            comfort: {
                level: document.getElementById('comfortLevel').value,
                noiseTarget: document.getElementById('noiseTarget').value
            },
            certifications: {
                leed: document.getElementById('certLEED').checked,
                breeam: document.getElementById('certBREEAM').checked,
                edge: document.getElementById('certEDGE').checked,
                passivhaus: document.getElementById('certPassivhaus').checked,
                well: document.getElementById('certWELL').checked,
                local: document.getElementById('certLocal').checked,
                none: document.getElementById('certNone').checked
            }
        },
        landscape: {
            concept: {
                style: document.getElementById('landscapeStyle').value,
                description: document.getElementById('landscapeConcept').value
            },
            vegetation: {
                trees: parseInt(document.getElementById('treeCount').value),
                smallTrees: parseInt(document.getElementById('smallTreeCount').value),
                bushes: parseInt(document.getElementById('bushCount').value),
                grassArea: parseFloat(document.getElementById('grassArea').value),
                flowers: parseInt(document.getElementById('flowerCount').value),
                totalGreen: parseFloat(document.getElementById('totalGreenArea').value),
                types: document.getElementById('plantTypes').value,
                zones: document.getElementById('plantZones').value
            },
            irrigation: {
                type: document.getElementById('irrigationType').value,
                zones: parseInt(document.getElementById('irrigationZones').value)
            },
            elements: {
                deck: document.getElementById('elDeck').checked,
                paths: document.getElementById('elPaths').checked,
                pergola: document.getElementById('elPergola').checked,
                pond: document.getElementById('elPond').checked,
                lights: document.getElementById('elLights').checked,
                seating: document.getElementById('elSeating').checked,
                wallGarden: document.getElementById('elWallGarden').checked,
                firepit: document.getElementById('elFirepit').checked,
                play: document.getElementById('elPlay').checked,
                meditation: document.getElementById('elMeditation').checked
            },
            lighting: document.getElementById('extLightStyle').value
        },
        budget: {
            total: parseFloat(document.getElementById('budgetTotal').value),
            costPerM2: parseFloat(document.getElementById('costPerM2').value),
            type: document.getElementById('budgetType').value,
            distribution: {
                foundation: parseInt(document.getElementById('budgetFoundation').value),
                structure: parseInt(document.getElementById('budgetStructure').value),
                walls: parseInt(document.getElementById('budgetWalls').value),
                roof: parseInt(document.getElementById('budgetRoof').value),
                carpentry: parseInt(document.getElementById('budgetCarpentry').value),
                floors: parseInt(document.getElementById('budgetFloors').value),
                plumbing: parseInt(document.getElementById('budgetPlumbing').value),
                electric: parseInt(document.getElementById('budgetElectric').value),
                hvac: parseInt(document.getElementById('budgetHVAC').value),
                finishes: parseInt(document.getElementById('budgetFinishes').value),
                landscape: parseInt(document.getElementById('budgetLandscape').value),
                misc: parseInt(document.getElementById('budgetMisc').value)
            },
            priority: document.getElementById('priority').value,
            contingency: parseInt(document.getElementById('contingency').value),
            notes: document.getElementById('budgetNotes').value,
            financing: {
                source: document.getElementById('fundingSource').value,
                schedule: document.getElementById('paymentSchedule').value
            }
        },
        schedule: {
            startDate: document.getElementById('startDate').value,
            durationMonths: parseInt(document.getElementById('durationMonths').value),
            endDate: document.getElementById('endDate').value,
            phases: {
                design: { weeks: parseInt(document.getElementById('phase1Weeks').value), start: document.getElementById('phase1Start').value },
                preConstruction: { weeks: parseInt(document.getElementById('phase2Weeks').value), start: document.getElementById('phase2Start').value },
                structure: { weeks: parseInt(document.getElementById('phase3Weeks').value), start: document.getElementById('phase3Start').value },
                closures: { weeks: parseInt(document.getElementById('phase4Weeks').value), start: document.getElementById('phase4Start').value },
                finishes: { weeks: parseInt(document.getElementById('phase5Weeks').value), start: document.getElementById('phase5Start').value },
                delivery: { weeks: parseInt(document.getElementById('phase6Weeks').value), start: document.getElementById('phase6Start').value }
            },
            milestones: document.getElementById('milestones').value,
            resources: {
                contractorType: document.getElementById('contractorType').value,
                supervision: document.getElementById('supervision').value
            }
        },
        notes: {
            clientVision: document.getElementById('clientVision').value,
            references: document.getElementById('references').value,
            moodBoard: document.getElementById('moodBoard').value,
            restrictions: document.getElementById('restrictions').value,
            mustHave: document.getElementById('mustHave').value,
            longTermVision: document.getElementById('longTermVision').value,
            additionalInfo: document.getElementById('additionalInfo').value
        }
    };
    return data;
}

function generateTXT() {
    const d = collectData();
    const now = new Date();
    const dateStr = now.toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' });

    const txt = `
${'='.repeat(80)}
              FICHA TÉCNICA COMPLETA DE PROYECTO ARQUITECTÓNICO
                    VIVIENDA CAMPESTRE PARAMÉTRICA
${'='.repeat(80)}

Fecha de generación: ${dateStr}
Nombre del proyecto: ${d.project.name}
Código: ${d.project.code}
Cliente: ${d.project.client || '[No especificado]'}
Ubicación: ${d.project.location || '[No especificado]'}

${'='.repeat(80)}
1. CONTEXTO Y SITIO
${'='.repeat(80)}

--- GEOMETRÍA DEL TERRENO ---
  • Largo: ${d.site.lot.length} m
  • Ancho: ${d.site.lot.width} m
  • Área total: ${d.site.lot.area} m²
  • Forma: ${d.site.lot.shape}
  ${d.site.lot.dimensions ? '  • Dimensiones: ' + d.site.lot.dimensions : ''}

--- TOPOGRAFÍA ---
  • Pendiente: ${d.site.topography.slope}
  • Dirección pendiente: ${d.site.topography.direction}
  • Elevación: ${d.site.topography.elevation} msnm
  • Tipo de suelo: ${d.site.topography.soilType}
  • Notas suelo: ${d.site.topography.soilNotes}

--- CLIMA ---
  • Tipo: ${d.site.climate.type}
  • Zona de altitud: ${d.site.climate.altitudeZone}
  • Temperaturas: ${d.site.climate.tempMin}°C min / ${d.site.climate.tempMax}°C max / ${d.site.climate.tempAvg}°C media
  • Precipitación anual: ${d.site.climate.rainfall} mm
  • Humedad relativa: ${d.site.climate.humidity}%
  • Horas de sol: ${d.site.climate.sunHours} h/año
  • Viento predominante: ${d.site.climate.windDirection} (${d.site.climate.windSpeed} km/h máx)
  • Zona sísmica: ${d.site.climate.seismicZone}
  • Riesgo natural: ${d.site.climate.riskZone}

--- ORIENTACIÓN ---
  • Orientación principal: ${d.site.orientation.main}
  • Trayectoria solar: ${d.site.orientation.sunPath}
  • Sombras: N:${d.site.orientation.shadeNorth?'SÍ':'NO'} S:${d.site.orientation.shadeSouth?'SÍ':'NO'} E:${d.site.orientation.shadeEast?'SÍ':'NO'} O:${d.site.orientation.shadeWest?'SÍ':'NO'}
  • Árboles sombra: ${d.site.orientation.shadeTrees?'SÍ':'NO'} | Montaña: ${d.site.orientation.shadeMountain?'SÍ':'NO'}

--- ENTORNO ---
  • Tipo de zona: ${d.site.surroundings.zoneType}
  • Vegetación: ${d.site.surroundings.vegetation?'SÍ':'NO'} | Tranquilo: ${d.site.surroundings.quiet?'SÍ':'NO'}
  • Buenas vistas: ${d.site.surroundings.viewGood?'SÍ':'NO'} | Ruido: ${d.site.surroundings.noise?'SÍ':'NO'}
  • Descripción: ${d.site.surroundings.description}

--- SERVICIOS ---
  • Agua: ${d.site.services.water?'SÍ':'NO'} | Alcantarillado: ${d.site.services.sewer?'SÍ':'NO'}
  • Electricidad: ${d.site.services.electric?'SÍ':'NO'} | Gas: ${d.site.services.gas?'SÍ':'NO'}
  • Internet: ${d.site.services.internet?'SÍ':'NO'} | Pavimento: ${d.site.services.paved?'SÍ':'NO'}
  • Alumbrado: ${d.site.services.streetLight?'SÍ':'NO'} | Recolección: ${d.site.services.garbage?'SÍ':'NO'}
  • Fuente agua: ${d.site.services.waterSource}
  • Sistema aguas: ${d.site.services.sewageSystem}

${'='.repeat(80)}
2. NORMATIVA Y REGULACIONES
${'='.repeat(80)}

--- MARCO REGULATORIO ---
  • Tipo: ${d.regulations.type}
  • Código: ${d.regulations.code || '[No especificado]'}
  • Zonificación: ${d.regulations.zoning}

--- RETIROS ---
  • Frontal: ${d.regulations.setbacks.front} m
  • Posterior: ${d.regulations.setbacks.back} m
  • Lateral: ${d.regulations.setbacks.side} m
  • Notas: ${d.regulations.setbacks.notes}

--- LÍMITES CONSTRUCTIVOS ---
  • Altura máxima: ${d.regulations.limits.maxHeight} m
  • Niveles máximos: ${d.regulations.limits.maxLevels}
  • Altura máx/nivel: ${d.regulations.limits.maxFloorHeight} m
  • Ocupación suelo: ${d.regulations.limits.maxCoverage}%
  • FSI/COS: ${d.regulations.limits.maxFSI}
  • GSI/CIS: ${d.regulations.limits.maxGSI}

--- ESTACIONAMIENTOS ---
  • Mínimos: ${d.regulations.parking.required}
  • Bicicletas: ${d.regulations.parking.bike}
  • Visitantes: ${d.regulations.parking.visitors}
  • Acceso: ${d.regulations.parking.accessType}

--- REQUISITOS ---
  • Accesibilidad: ${d.regulations.requirements.accessibility?'SÍ':'NO'}
  • Incendios: ${d.regulations.requirements.fire?'SÍ':'NO'}
  • Sísmico: ${d.regulations.requirements.seismic?'SÍ':'NO'}
  • Energía: ${d.regulations.requirements.energy?'SÍ':'NO'}
  • Aguas: ${d.regulations.requirements.water?'SÍ':'NO'}
  • Verdes: ${d.regulations.requirements.green?'SÍ':'NO'}
  • Ruido: ${d.regulations.requirements.noise?'SÍ':'NO'}
  • Ambiental: ${d.regulations.requirements.environmental?'SÍ':'NO'}
  • Patrimonio: ${d.regulations.requirements.historic?'SÍ':'NO'}
  • Altura adicional: ${d.regulations.requirements.heightLimit?'SÍ':'NO'}
  • Notas: ${d.regulations.requirements.notes}

--- ÁREAS VERDES ---
  • Mínima requerida: ${d.regulations.greenArea.required} m²
  • Retiro con vegetación: ${d.regulations.greenArea.setbackGreen}

${'='.repeat(80)}
3. PROGRAMA ARQUITECTÓNICO
${'='.repeat(80)}

--- GENERAL ---
  • Área total: ${d.program.general.totalArea} m² (Máx. 130 m²)
  • Niveles: ${d.program.general.levels}
  • Altura/nivel: ${d.program.general.floorHeight} m
  • Altura total: ${d.program.general.totalHeight} m
  • Altura libre: ${d.program.general.ceilingHeight} m
  • Espesor losa: ${d.program.general.slabThickness} m
  • Flexibilidad: ${d.program.flexibility}

--- NIVEL 1 (PLANTA BAJA) - ${d.program.level1.area} m² ---
  • Uso: ${d.program.level1.use}
  • Espacios:
${d.program.level1.program.split('\n').map(l => '    ' + l).join('\n')}
  • Notas: ${d.program.level1.notes}

--- NIVEL 2 (PLANTA ALTA) - ${d.program.level2.area} m² ---
  • Uso: ${d.program.level2.use}
  • Espacios:
${d.program.level2.program.split('\n').map(l => '    ' + l).join('\n')}
  • Notas: ${d.program.level2.notes}

--- ESPACIOS ESPECIALES ---
  • Terraza: ${d.program.spaces.terrace?'SÍ':'NO'} | Patio interior: ${d.program.spaces.patio?'SÍ':'NO'}
  • Garaje: ${d.program.spaces.garage?'SÍ':'NO'} | Bodega: ${d.program.spaces.storage?'SÍ':'NO'}
  • Piscina: ${d.program.spaces.pool?'SÍ':'NO'} | Huerto: ${d.program.spaces.garden?'SÍ':'NO'}
  • BBQ: ${d.program.spaces.bbq?'SÍ':'NO'} | Gimnasio: ${d.program.spaces.gym?'SÍ':'NO'}
  • Home office: ${d.program.spaces.office?'SÍ':'NO'}

--- ZONAS HÚMEDAS ---
  • Baños: ${d.program.wetZones.bathrooms}
  • Cocinas: ${d.program.wetZones.kitchenCount}
  • Distribución: ${d.program.wetZones.distribution}

--- REQUISITOS ESPECIALES ---
${d.program.special}

${'='.repeat(80)}
4. PARÁMETROS DE DISEÑO
${'='.repeat(80)}

--- CONCEPTO ---
  • Estilo: ${d.design.concept.style}
  • Filosofía: ${d.design.concept.philosophy}
  • Descripción: ${d.design.concept.description}

--- PROPORCIONES ---
  • Sistema: ${d.design.proportions.system}
  • Módulo base: ${d.design.proportions.moduleSize} m
  • Proporción fachada: ${d.design.proportions.facade}
  • Volumetría: ${d.design.proportions.volumetry}

--- CUBIERTA ---
  • Tipo: ${d.design.roof.type}
  • Material: ${d.design.roof.material}
  • Inclinación: ${d.design.roof.pitch}°
  • Volado: ${d.design.roof.overhang} m
  • Altura cubierta: ${d.design.roof.height} m

--- VENTANAS ---
  • Dimensiones: ${d.design.windows.width} m × ${d.design.windows.height} m
  • Ratio ventana/muro: ${d.design.windows.ratio}%
  • Orientación principal: ${d.design.windows.orientation}
  • Tipo: ${d.design.windows.type}
  • Especiales: 
    Piso a techo: ${d.design.windows.specials.floorToCeiling?'SÍ':'NO'}
    Claraboya: ${d.design.windows.specials.clerestory?'SÍ':'NO'}
    Tragaluz: ${d.design.windows.specials.skylight?'SÍ':'NO'}
    Esquina: ${d.design.windows.specials.corner?'SÍ':'NO'}
    Salediza: ${d.design.windows.specials.bay?'SÍ':'NO'}
    Cinta: ${d.design.windows.specials.ribbon?'SÍ':'NO'}

--- PUERTAS ---
  • Principal: ${d.design.doors.main} (${d.design.doors.mainHeight} m alto)
  • Interiores: ${d.design.doors.interior}

--- FACHADA ---
${d.design.facade}

${'='.repeat(80)}
5. PALETA DE MATERIALES
${'='.repeat(80)}

--- MUROS ---
  • Sistema: ${d.materials.walls.structural}
  • Espesor: ${d.materials.walls.thickness} cm
  • Acabado principal: ${d.materials.walls.finish}
  • Textura: ${d.materials.walls.texture}

--- ACENTOS ---
  • Material: ${d.materials.accent.material}
  • Ubicación: ${d.materials.accent.location}

--- PISOS ---
  • Interior: ${d.materials.floors.interior}
  • Exterior: ${d.materials.floors.exterior}

--- VIDRIOS ---
  • Tipo: ${d.materials.glass.type}
  • Espesor: ${d.materials.glass.thickness}

--- CARPINTERÍA METÁLICA ---
  • Material perfiles: ${d.materials.frames.material}
  • Color: ${d.materials.frames.color}

--- NOTAS ---
${d.materials.notes}

--- CERTIFICACIONES MATERIALES ---
  • Madera FSC: ${d.materials.certifications.fsc?'SÍ':'NO'}
  • Reciclados: ${d.materials.certifications.recycle?'SÍ':'NO'}
  • Locales: ${d.materials.certifications.local?'SÍ':'NO'}
  • Bajas VOC: ${d.materials.certifications.lowVOC?'SÍ':'NO'}
  • Energy Star: ${d.materials.certifications.energyStar?'SÍ':'NO'}

${'='.repeat(80)}
6. SOSTENIBILIDAD Y CONFORT
${'='.repeat(80)}

--- ESTRATEGIAS PASIVAS ---
  • Ventilación cruzada: ${d.sustainability.passive.crossVentilation?'SÍ':'NO'}
  • Efecto chimenea: ${d.sustainability.passive.stackVentilation?'SÍ':'NO'}
  • Iluminación natural: ${d.sustainability.passive.naturalLight?'SÍ':'NO'}
  • Ganancia solar: ${d.sustainability.passive.solarGain?'SÍ':'NO'}
  • Masa térmica: ${d.sustainability.passive.thermalMass?'SÍ':'NO'}
  • Sombreamiento: ${d.sustainability.passive.shading?'SÍ':'NO'}
  • Enfriamiento evaporativo: ${d.sustainability.passive.evaporative?'SÍ':'NO'}
  • Cubierta verde: ${d.sustainability.passive.greenRoof?'SÍ':'NO'}
  • Fachada verde: ${d.sustainability.passive.greenFacade?'SÍ':'NO'}
  • Tubos enterrados: ${d.sustainability.passive.earthTube?'SÍ':'NO'}
  • Ventilación nocturna: ${d.sustainability.passive.nightFlush?'SÍ':'NO'}
  • Brise-soleil: ${d.sustainability.passive.sunBreakers?'SÍ':'NO'}

--- ESTRATEGIAS ACTIVAS ---
  • Solar fotovoltaico: ${d.sustainability.active.solarPV?'SÍ':'NO'}
  • Calentador solar: ${d.sustainability.active.solarHeat?'SÍ':'NO'}
  • Bomba de calor: ${d.sustainability.active.heatPump?'SÍ':'NO'}
  • Recolección lluvia: ${d.sustainability.active.rainwater?'SÍ':'NO'}
  • Aguas grises: ${d.sustainability.active.grayWater?'SÍ':'NO'}
  • Domótica: ${d.sustainability.active.smartHome?'SÍ':'NO'}
  • LED 100%: ${d.sustainability.active.led?'SÍ':'NO'}
  • Cargador EV: ${d.sustainability.active.evCharger?'SÍ':'NO'}

--- EFICIENCIA ENERGÉTICA ---
  • Meta: ${d.sustainability.energy.target}
  • Aislamiento: ${d.sustainability.energy.insulation}
  • U muro: ${d.sustainability.energy.uWall} W/m²K
  • U cubierta: ${d.sustainability.energy.uRoof} W/m²K
  • U ventana: ${d.sustainability.energy.uWindow} W/m²K

--- CONFORT ---
  • Nivel: ${d.sustainability.comfort.level}
  • Ruido objetivo: ${d.sustainability.comfort.noiseTarget} dB

--- CERTIFICACIONES ---
  • LEED: ${d.sustainability.certifications.leed?'SÍ':'NO'}
  • BREEAM: ${d.sustainability.certifications.breeam?'SÍ':'NO'}
  • EDGE: ${d.sustainability.certifications.edge?'SÍ':'NO'}
  • Passivhaus: ${d.sustainability.certifications.passivhaus?'SÍ':'NO'}
  • WELL: ${d.sustainability.certifications.well?'SÍ':'NO'}
  • Local: ${d.sustainability.certifications.local?'SÍ':'NO'}
  • Ninguna: ${d.sustainability.certifications.none?'SÍ':'NO'}

${'='.repeat(80)}
7. PAISAJISMO Y VEGETACIÓN
${'='.repeat(80)}

--- CONCEPTO ---
  • Estilo: ${d.landscape.concept.style}
  • Descripción: ${d.landscape.concept.description}

--- VEGETACIÓN ---
  • Árboles grandes (>4m): ${d.landscape.vegetation.trees}
  • Árboles pequeños (2-4m): ${d.landscape.vegetation.smallTrees}
  • Arbustos: ${d.landscape.vegetation.bushes}
  • Césped: ${d.landscape.vegetation.grassArea} m²
  • Flores/macetas: ${d.landscape.vegetation.flowers}
  • Área verde total: ${d.landscape.vegetation.totalGreen} m²
  • Tipos: ${d.landscape.vegetation.types}
  • Zonificación: ${d.landscape.vegetation.zones}

--- RIEGO ---
  • Tipo: ${d.landscape.irrigation.type}
  • Zonas: ${d.landscape.irrigation.zones}

--- ELEMENTOS ---
  • Deck: ${d.landscape.elements.deck?'SÍ':'NO'} | Senderos: ${d.landscape.elements.paths?'SÍ':'NO'}
  • Pérgola: ${d.landscape.elements.pergola?'SÍ':'NO'} | Estanque: ${d.landscape.elements.pond?'SÍ':'NO'}
  • Iluminación: ${d.landscape.elements.lights?'SÍ':'NO'} | Asientos: ${d.landscape.elements.seating?'SÍ':'NO'}
  • Green wall: ${d.landscape.elements.wallGarden?'SÍ':'NO'} | Firepit: ${d.landscape.elements.firepit?'SÍ':'NO'}
  • Juegos: ${d.landscape.elements.play?'SÍ':'NO'} | Meditación: ${d.landscape.elements.meditation?'SÍ':'NO'}

--- ILUMINACIÓN ---
  • Estilo: ${d.landscape.lighting}

${'='.repeat(80)}
8. PRESUPUESTO Y COSTOS
${'='.repeat(80)}

--- GENERAL ---
  • Presupuesto total: USD ${d.budget.total.toLocaleString()}
  • Costo/m²: USD ${d.budget.costPerM2}
  • Tipo: ${d.budget.type}
  • Prioridad: ${d.budget.priority}
  • Contingencia: ${d.budget.contingency}%

--- DISTRIBUCIÓN ---
  • Cimentación: ${d.budget.distribution.foundation}%
  • Estructura: ${d.budget.distribution.structure}%
  • Muros: ${d.budget.distribution.walls}%
  • Cubierta: ${d.budget.distribution.roof}%
  • Carpintería: ${d.budget.distribution.carpentry}%
  • Pisos: ${d.budget.distribution.floors}%
  • Plomería: ${d.budget.distribution.plumbing}%
  • Electricidad: ${d.budget.distribution.electric}%
  • HVAC: ${d.budget.distribution.hvac}%
  • Acabados: ${d.budget.distribution.finishes}%
  • Paisajismo: ${d.budget.distribution.landscape}%
  • Diversos: ${d.budget.distribution.misc}%

--- NOTAS ---
${d.budget.notes}

--- FINANCIAMIENTO ---
  • Fuente: ${d.budget.financing.source}
  • Calendario: ${d.budget.financing.schedule}

${'='.repeat(80)}
9. CRONOGRAMA Y ACTIVIDADES
${'='.repeat(80)}

--- PROGRAMACIÓN ---
  • Inicio: ${d.schedule.startDate}
  • Duración: ${d.schedule.durationMonths} meses
  • Entrega: ${d.schedule.endDate}

--- FASES ---
  1. Diseño: ${d.schedule.phases.design.weeks} semanas (${d.schedule.phases.design.start})
  2. Pre-obra: ${d.schedule.phases.preConstruction.weeks} semanas (${d.schedule.phases.preConstruction.start})
  3. Estructura: ${d.schedule.phases.structure.weeks} semanas (${d.schedule.phases.structure.start})
  4. Cerramientos: ${d.schedule.phases.closures.weeks} semanas (${d.schedule.phases.closures.start})
  5. Acabados: ${d.schedule.phases.finishes.weeks} semanas (${d.schedule.phases.finishes.start})
  6. Entrega: ${d.schedule.phases.delivery.weeks} semanas (${d.schedule.phases.delivery.start})

--- HITOS ---
${d.schedule.milestones}

--- RECURSOS ---
  • Contratista: ${d.schedule.resources.contractorType}
  • Supervisión: ${d.schedule.resources.supervision}

${'='.repeat(80)}
10. NOTAS Y CONSIDERACIONES ADICIONALES
${'='.repeat(80)}

--- VISIÓN DEL CLIENTE ---
${d.notes.clientVision}

--- REFERENCIAS ---
${d.notes.references}

--- MOOD BOARD ---
${d.notes.moodBoard}

--- RESTRICCIONES ---
${d.notes.restrictions}

--- MUST-HAVES ---
${d.notes.mustHave}

--- VISIÓN A LARGO PLAZO ---
${d.notes.longTermVision}

--- INFORMACIÓN ADICIONAL ---
${d.notes.additionalInfo}

${'='.repeat(80)}
                    FIN DE LA FICHA TÉCNICA COMPLETA
${'='.repeat(80)}

Este documento contiene todos los parámetros necesarios para el desarrollo
del proyecto arquitectónico. Puede ser utilizado como:
  • Briefing para el equipo de diseño
  • Base para parametrización en Grasshopper / Rhino
  • Entrada para software BIM (Revit, ArchiCAD)
  • Especificación para licitación de obra

Generado: ${dateStr}
Proyecto: ${d.project.name}
Código: ${d.project.code}
${'='.repeat(80)}
`;
    return txt.trim();
}

function exportTXT() {
    const txt = generateTXT();
    const blob = new Blob([txt], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ficha-completa-${document.getElementById('projectName').value.replace(/\s+/g, '-').toLowerCase()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function exportJSON() {
    const data = collectData();
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `parametros-completos-${document.getElementById('projectName').value.replace(/\s+/g, '-').toLowerCase()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function loadFromJSON(data) {
    if (data.project) {
        if (data.project.name) document.getElementById('projectName').value = data.project.name;
        if (data.project.code) document.getElementById('projectCode').value = data.project.code;
        if (data.project.client) document.getElementById('clientName').value = data.project.client;
        if (data.project.location) document.getElementById('location').value = data.project.location;
    }
    if (data.site) {
        if (data.site.lot) {
            if (data.site.lot.length) document.getElementById('lotLength').value = data.site.lot.length;
            if (data.site.lot.width) document.getElementById('lotWidth').value = data.site.lot.width;
            if (data.site.lot.shape) document.getElementById('lotShape').value = data.site.lot.shape;
            if (data.site.lot.dimensions) document.getElementById('lotDimensions').value = data.site.lot.dimensions;
        }
        if (data.site.topography) {
            if (data.site.topography.slope) document.getElementById('topography').value = data.site.topography.slope;
            if (data.site.topography.direction) document.getElementById('slopeDirection').value = data.site.topography.direction;
            if (data.site.topography.elevation) document.getElementById('elevation').value = data.site.topography.elevation;
            if (data.site.topography.soilType) document.getElementById('soilType').value = data.site.topography.soilType;
            if (data.site.topography.soilNotes) document.getElementById('soilNotes').value = data.site.topography.soilNotes;
        }
        if (data.site.climate) {
            if (data.site.climate.type) document.getElementById('climate').value = data.site.climate.type;
            if (data.site.climate.altitudeZone) document.getElementById('altitudeZone').value = data.site.climate.altitudeZone;
            if (data.site.climate.tempMax) document.getElementById('tempMax').value = data.site.climate.tempMax;
            if (data.site.climate.tempMin) document.getElementById('tempMin').value = data.site.climate.tempMin;
            if (data.site.climate.tempAvg) document.getElementById('tempAvg').value = data.site.climate.tempAvg;
            if (data.site.climate.rainfall) document.getElementById('rainfall').value = data.site.climate.rainfall;
            if (data.site.climate.humidity) document.getElementById('humidity').value = data.site.climate.humidity;
            if (data.site.climate.sunHours) document.getElementById('sunHours').value = data.site.climate.sunHours;
            if (data.site.climate.windDirection) document.getElementById('windDirection').value = data.site.climate.windDirection;
            if (data.site.climate.windSpeed) document.getElementById('windSpeed').value = data.site.climate.windSpeed;
            if (data.site.climate.seismicZone) document.getElementById('seismicZone').value = data.site.climate.seismicZone;
            if (data.site.climate.riskZone) document.getElementById('riskZone').value = data.site.climate.riskZone;
        }
        if (data.site.orientation) {
            if (data.site.orientation.main) document.getElementById('orientation').value = data.site.orientation.main;
            if (data.site.orientation.sunPath) document.getElementById('sunPath').value = data.site.orientation.sunPath;
        }
        if (data.site.surroundings) {
            if (data.site.surroundings.zoneType) document.getElementById('zoneType').value = data.site.surroundings.zoneType;
            if (data.site.surroundings.description) document.getElementById('surroundings').value = data.site.surroundings.description;
        }
        if (data.site.services) {
            if (data.site.services.waterSource) document.getElementById('waterSource').value = data.site.services.waterSource;
            if (data.site.services.sewageSystem) document.getElementById('sewageSystem').value = data.site.services.sewageSystem;
        }
    }
    if (data.regulations) {
        if (data.regulations.type) document.getElementById('regulationType').value = data.regulations.type;
        if (data.regulations.code) document.getElementById('regulationCode').value = data.regulations.code;
        if (data.regulations.zoning) document.getElementById('zoning').value = data.regulations.zoning;
        if (data.regulations.setbacks) {
            if (data.regulations.setbacks.front !== undefined) document.getElementById('setbackFront').value = data.regulations.setbacks.front;
            if (data.regulations.setbacks.back !== undefined) document.getElementById('setbackBack').value = data.regulations.setbacks.back;
            if (data.regulations.setbacks.side !== undefined) document.getElementById('setbackSide').value = data.regulations.setbacks.side;
            if (data.regulations.setbacks.notes) document.getElementById('setbackNotes').value = data.regulations.setbacks.notes;
        }
        if (data.regulations.limits) {
            if (data.regulations.limits.maxHeight) document.getElementById('maxHeight').value = data.regulations.limits.maxHeight;
            if (data.regulations.limits.maxLevels) document.getElementById('maxLevels').value = data.regulations.limits.maxLevels;
            if (data.regulations.limits.maxFloorHeight) document.getElementById('maxFloorHeight').value = data.regulations.limits.maxFloorHeight;
            if (data.regulations.limits.maxCoverage) document.getElementById('maxCoverage').value = data.regulations.limits.maxCoverage;
            if (data.regulations.limits.maxFSI) document.getElementById('maxFSI').value = data.regulations.limits.maxFSI;
            if (data.regulations.limits.maxGSI) document.getElementById('maxGSI').value = data.regulations.limits.maxGSI;
        }
        if (data.regulations.parking) {
            if (data.regulations.parking.required !== undefined) document.getElementById('parking').value = data.regulations.parking.required;
            if (data.regulations.parking.bike !== undefined) document.getElementById('bikeParking').value = data.regulations.parking.bike;
            if (data.regulations.parking.visitors !== undefined) document.getElementById('visitorsParking').value = data.regulations.parking.visitors;
            if (data.regulations.parking.accessType) document.getElementById('accessType').value = data.regulations.parking.accessType;
        }
        if (data.regulations.requirements) {
            if (data.regulations.requirements.notes) document.getElementById('reqNotes').value = data.regulations.requirements.notes;
        }
    }
    if (data.program) {
        if (data.program.general) {
            if (data.program.general.totalArea) document.getElementById('totalArea').value = data.program.general.totalArea;
            if (data.program.general.levels) document.getElementById('levels').value = data.program.general.levels;
            if (data.program.general.floorHeight) document.getElementById('floorHeight').value = data.program.general.floorHeight;
            if (data.program.general.ceilingHeight) document.getElementById('ceilingHeight').value = data.program.general.ceilingHeight;
            if (data.program.general.slabThickness) document.getElementById('slabThickness').value = data.program.general.slabThickness;
        }
        if (data.program.level1) {
            if (data.program.level1.area) document.getElementById('level1Area').value = data.program.level1.area;
            if (data.program.level1.use) document.getElementById('level1Use').value = data.program.level1.use;
            if (data.program.level1.program) document.getElementById('level1Program').value = data.program.level1.program;
            if (data.program.level1.notes) document.getElementById('level1Notes').value = data.program.level1.notes;
        }
        if (data.program.level2) {
            if (data.program.level2.area) document.getElementById('level2Area').value = data.program.level2.area;
            if (data.program.level2.use) document.getElementById('level2Use').value = data.program.level2.use;
            if (data.program.level2.program) document.getElementById('level2Program').value = data.program.level2.program;
            if (data.program.level2.notes) document.getElementById('level2Notes').value = data.program.level2.notes;
        }
        if (data.program.wetZones) {
            if (data.program.wetZones.bathrooms) document.getElementById('bathrooms').value = data.program.wetZones.bathrooms;
            if (data.program.wetZones.kitchenCount) document.getElementById('kitchenCount').value = data.program.wetZones.kitchenCount;
            if (data.program.wetZones.distribution) document.getElementById('wetZones').value = data.program.wetZones.distribution;
        }
        if (data.program.special) document.getElementById('specialReq').value = data.program.special;
        if (data.program.flexibility) document.getElementById('flexibility').value = data.program.flexibility;
    }
    if (data.design) {
        if (data.design.concept) {
            if (data.design.concept.style) document.getElementById('designStyle').value = data.design.concept.style;
            if (data.design.concept.philosophy) document.getElementById('designPhilosophy').value = data.design.concept.philosophy;
            if (data.design.concept.description) document.getElementById('designConcept').value = data.design.concept.description;
        }
        if (data.design.proportions) {
            if (data.design.proportions.system) document.getElementById('proportionSystem').value = data.design.proportions.system;
            if (data.design.proportions.moduleSize) document.getElementById('moduleSize').value = data.design.proportions.moduleSize;
            if (data.design.proportions.facade) document.getElementById('facadeProportion').value = data.design.proportions.facade;
            if (data.design.proportions.volumetry) document.getElementById('volumetry').value = data.design.proportions.volumetry;
        }
        if (data.design.roof) {
            if (data.design.roof.type) document.getElementById('roofType').value = data.design.roof.type;
            if (data.design.roof.material) document.getElementById('roofMaterial').value = data.design.roof.material;
            if (data.design.roof.pitch !== undefined) document.getElementById('roofPitch').value = data.design.roof.pitch;
            if (data.design.roof.overhang !== undefined) document.getElementById('roofOverhang').value = data.design.roof.overhang;
            if (data.design.roof.height) document.getElementById('roofHeight').value = data.design.roof.height;
        }
        if (data.design.windows) {
            if (data.design.windows.width) document.getElementById('windowWidth').value = data.design.windows.width;
            if (data.design.windows.height) document.getElementById('windowHeight').value = data.design.windows.height;
            if (data.design.windows.ratio) document.getElementById('windowRatio').value = data.design.windows.ratio;
            if (data.design.windows.orientation) document.getElementById('windowOrientation').value = data.design.windows.orientation;
            if (data.design.windows.type) document.getElementById('windowType').value = data.design.windows.type;
        }
        if (data.design.doors) {
            if (data.design.doors.main) document.getElementById('mainDoor').value = data.design.doors.main;
            if (data.design.doors.mainHeight) document.getElementById('mainDoorHeight').value = data.design.doors.mainHeight;
            if (data.design.doors.interior) document.getElementById('interiorDoors').value = data.design.doors.interior;
        }
        if (data.design.facade) document.getElementById('facadeTreatment').value = data.design.facade;
    }
    if (data.materials) {
        if (data.materials.walls) {
            if (data.materials.walls.structural) document.getElementById('wallStructural').value = data.materials.walls.structural;
            if (data.materials.walls.thickness) document.getElementById('wallThickness').value = data.materials.walls.thickness;
            if (data.materials.walls.finish) document.getElementById('wallMaterial').value = data.materials.walls.finish;
            if (data.materials.walls.texture) document.getElementById('wallFinish').value = data.materials.walls.texture;
        }
        if (data.materials.accent) {
            if (data.materials.accent.material) document.getElementById('accentMaterial').value = data.materials.accent.material;
            if (data.materials.accent.location) document.getElementById('accentLocation').value = data.materials.accent.location;
        }
        if (data.materials.floors) {
            if (data.materials.floors.interior) document.getElementById('floorInterior').value = data.materials.floors.interior;
            if (data.materials.floors.exterior) document.getElementById('floorExt').value = data.materials.floors.exterior;
        }
        if (data.materials.glass) {
            if (data.materials.glass.type) document.getElementById('glassType').value = data.materials.glass.type;
            if (data.materials.glass.thickness) document.getElementById('glassThickness').value = data.materials.glass.thickness;
        }
        if (data.materials.frames) {
            if (data.materials.frames.material) document.getElementById('frameMaterial').value = data.materials.frames.material;
            if (data.materials.frames.color) document.getElementById('frameColor').value = data.materials.frames.color;
        }
        if (data.materials.notes) document.getElementById('materialNotes').value = data.materials.notes;
    }
    if (data.sustainability) {
        if (data.sustainability.energy) {
            if (data.sustainability.energy.target) document.getElementById('energyTarget').value = data.sustainability.energy.target;
            if (data.sustainability.energy.insulation) document.getElementById('insulationLevel').value = data.sustainability.energy.insulation;
            if (data.sustainability.energy.uWall) document.getElementById('uWall').value = data.sustainability.energy.uWall;
            if (data.sustainability.energy.uRoof) document.getElementById('uRoof').value = data.sustainability.energy.uRoof;
            if (data.sustainability.energy.uWindow) document.getElementById('uWindow').value = data.sustainability.energy.uWindow;
        }
        if (data.sustainability.comfort) {
            if (data.sustainability.comfort.level) document.getElementById('comfortLevel').value = data.sustainability.comfort.level;
            if (data.sustainability.comfort.noiseTarget) document.getElementById('noiseTarget').value = data.sustainability.comfort.noiseTarget;
        }
    }
    if (data.landscape) {
        if (data.landscape.concept) {
            if (data.landscape.concept.style) document.getElementById('landscapeStyle').value = data.landscape.concept.style;
            if (data.landscape.concept.description) document.getElementById('landscapeConcept').value = data.landscape.concept.description;
        }
        if (data.landscape.vegetation) {
            if (data.landscape.vegetation.trees !== undefined) document.getElementById('treeCount').value = data.landscape.vegetation.trees;
            if (data.landscape.vegetation.smallTrees !== undefined) document.getElementById('smallTreeCount').value = data.landscape.vegetation.smallTrees;
            if (data.landscape.vegetation.bushes !== undefined) document.getElementById('bushCount').value = data.landscape.vegetation.bushes;
            if (data.landscape.vegetation.grassArea !== undefined) document.getElementById('grassArea').value = data.landscape.vegetation.grassArea;
            if (data.landscape.vegetation.flowers !== undefined) document.getElementById('flowerCount').value = data.landscape.vegetation.flowers;
            if (data.landscape.vegetation.types) document.getElementById('plantTypes').value = data.landscape.vegetation.types;
            if (data.landscape.vegetation.zones) document.getElementById('plantZones').value = data.landscape.vegetation.zones;
        }
        if (data.landscape.irrigation) {
            if (data.landscape.irrigation.type) document.getElementById('irrigationType').value = data.landscape.irrigation.type;
            if (data.landscape.irrigation.zones) document.getElementById('irrigationZones').value = data.landscape.irrigation.zones;
        }
        if (data.landscape.lighting) document.getElementById('extLightStyle').value = data.landscape.lighting;
    }
    if (data.budget) {
        if (data.budget.total) document.getElementById('budgetTotal').value = data.budget.total;
        if (data.budget.type) document.getElementById('budgetType').value = data.budget.type;
        if (data.budget.priority) document.getElementById('priority').value = data.budget.priority;
        if (data.budget.contingency !== undefined) document.getElementById('contingency').value = data.budget.contingency;
        if (data.budget.notes) document.getElementById('budgetNotes').value = data.budget.notes;
        if (data.budget.financing) {
            if (data.budget.financing.source) document.getElementById('fundingSource').value = data.budget.financing.source;
            if (data.budget.financing.schedule) document.getElementById('paymentSchedule').value = data.budget.financing.schedule;
        }
        if (data.budget.distribution) {
            if (data.budget.distribution.foundation !== undefined) document.getElementById('budgetFoundation').value = data.budget.distribution.foundation;
            if (data.budget.distribution.structure !== undefined) document.getElementById('budgetStructure').value = data.budget.distribution.structure;
            if (data.budget.distribution.walls !== undefined) document.getElementById('budgetWalls').value = data.budget.distribution.walls;
            if (data.budget.distribution.roof !== undefined) document.getElementById('budgetRoof').value = data.budget.distribution.roof;
            if (data.budget.distribution.carpentry !== undefined) document.getElementById('budgetCarpentry').value = data.budget.distribution.carpentry;
            if (data.budget.distribution.floors !== undefined) document.getElementById('budgetFloors').value = data.budget.distribution.floors;
            if (data.budget.distribution.plumbing !== undefined) document.getElementById('budgetPlumbing').value = data.budget.distribution.plumbing;
            if (data.budget.distribution.electric !== undefined) document.getElementById('budgetElectric').value = data.budget.distribution.electric;
            if (data.budget.distribution.hvac !== undefined) document.getElementById('budgetHVAC').value = data.budget.distribution.hvac;
            if (data.budget.distribution.finishes !== undefined) document.getElementById('budgetFinishes').value = data.budget.distribution.finishes;
            if (data.budget.distribution.landscape !== undefined) document.getElementById('budgetLandscape').value = data.budget.distribution.landscape;
            if (data.budget.distribution.misc !== undefined) document.getElementById('budgetMisc').value = data.budget.distribution.misc;
        }
    }
    if (data.schedule) {
        if (data.schedule.startDate) document.getElementById('startDate').value = data.schedule.startDate;
        if (data.schedule.durationMonths) document.getElementById('durationMonths').value = data.schedule.durationMonths;
        if (data.schedule.milestones) document.getElementById('milestones').value = data.schedule.milestones;
        if (data.schedule.resources) {
            if (data.schedule.resources.contractorType) document.getElementById('contractorType').value = data.schedule.resources.contractorType;
            if (data.schedule.resources.supervision) document.getElementById('supervision').value = data.schedule.resources.supervision;
        }
    }
    if (data.notes) {
        if (data.notes.clientVision) document.getElementById('clientVision').value = data.notes.clientVision;
        if (data.notes.references) document.getElementById('references').value = data.notes.references;
        if (data.notes.moodBoard) document.getElementById('moodBoard').value = data.notes.moodBoard;
        if (data.notes.restrictions) document.getElementById('restrictions').value = data.notes.restrictions;
        if (data.notes.mustHave) document.getElementById('mustHave').value = data.notes.mustHave;
        if (data.notes.longTermVision) document.getElementById('longTermVision').value = data.notes.longTermVision;
        if (data.notes.additionalInfo) document.getElementById('additionalInfo').value = data.notes.additionalInfo;
    }

    document.getElementById('lotLength').dispatchEvent(new Event('input'));
    document.getElementById('levels').dispatchEvent(new Event('input'));
    document.getElementById('totalArea').dispatchEvent(new Event('input'));
}

// DB INTEGRATION
const API = 'http://localhost:5000/api';
let DB_PROJECT_ID = null;
(function(){
  const params = new URLSearchParams(window.location.search);
  const pid = params.get('project_id');
  if (pid) {
    DB_PROJECT_ID = parseInt(pid);
    var bar = document.getElementById('dbBar');
    if (bar) {
      bar.style.display = 'flex';
      document.getElementById('dbInfo').textContent = 'Proyecto #' + DB_PROJECT_ID + ' | Conectado a BD';
      loadDT();
    }
  }
})();

async function saveDT() {
  if (!DB_PROJECT_ID) return alert('No hay proyecto vinculado. Abre desde el Dashboard.');
  var data = collectData();
  try {
    const res = await fetch(API + '/projects/' + DB_PROJECT_ID + '/dt', {
      method: 'PUT', headers: {'Content-Type':'application/json'},
      body: JSON.stringify(data)
    });
    if (!res.ok) throw await res.text();
    document.getElementById('dbInfo').textContent = 'Proyecto #' + DB_PROJECT_ID + ' | Guardado en BD';
  } catch(e) {
    alert('Error al guardar: ' + e);
  }
}

async function loadDT() {
  if (!DB_PROJECT_ID) return;
  try {
    const res = await fetch(API + '/projects/' + DB_PROJECT_ID + '/dt');
    if (!res.ok) throw await res.text();
    const data = await res.json();
    if (!data || Object.keys(data).length === 0) {
      document.getElementById('dbInfo').textContent = 'Proyecto #' + DB_PROJECT_ID + ' | Sin datos previos';
      return;
    }
    loadFromJSON(data);
    document.getElementById('dbInfo').textContent = 'Proyecto #' + DB_PROJECT_ID + ' | Datos cargados';
  } catch(e) {
    console.error('Error loading DT:', e);
  }
}
